#!/usr/bin/env python
import pathlib
from pathlib import Path
from urllib import parse
import subprocess
import os
import sys
import random
import re
from os.path import exists
from bisect import bisect_left, bisect_right
import sqlite3

MATCH_RATE = 0.7

'''
Contains a cache of song values. This will change depending on the search terms
'''
songVals = {}

'''
A sorting method for songs. It works by pushing file names with more matches up higher.

@param song -   The song to evaluate
@param terms -  The search terms to use.
@return A tuple containing the number of matches that were made as well as the
        total weighted value.
'''
def getSongValue(song, terms):
    if not "terms" in songVals or songVals["terms"] != terms:
        #if "terms" in songVals:
            #print("%s is not %s, clearing" % (terms, songVals["terms"]))
        #else:
            #print("Setting terms to %s" % (terms))
        songVals.clear()
        songVals["terms"] = terms
    val = 0
    sortval = 0
    if song in songVals:
        val, sortval = songVals[song[1]][0]
    else:
        #print(song[1])
        #print('\t', end='')
        for arg in terms:
            i = 1
            for part in song[3:]:
                part = re.sub('[^A-Za-z ]', '', part).lower()
                if arg in part:
                    val += 1
                    # This helps make title matches more valuable
                    sortval += 3 - 1
                    #print("%d %s - %s" % (val, arg, part), end="\t")
                i += 1
        songVals[song[1]] = (val, sortval)
        #print()
    # Double every point received by a playlist
    if song[0] == True:
        val *= 2
    return (val, sortval)

'''
Merges certain words into one. This is helpful for voice commands
'''
def __mergeWords(argList):
    i = 0
    quoting = False
    while i < len(argList):
        # Merge underscore for handling later
        if quoting:
            if argList[i] != "unquote":
                argList[i - 1] = argList[i - 1] + " " + argList[i]
            else:
                quoting = False
            del argList[i]
            i -= 1
        elif argList[i] == "quote":
            quoting = True
            del argList[i]
        elif i < len(argList) - 1 and argList[i] == "under" and argList[i + 1] == "score":
            argList[i] = "underscore"
            del argList[i + 1]
        elif i < len(argList) - 1 and argList[i] == "play" and argList[i + 1] == "list":
            argList[i] = "playlist"
            del argList[i + 1]
        if argList[i] == "dot":
            argList[i - 1] = argList[i - 1] + "."
            del argList[i]
            i -= 1
        elif argList[i] == "underscore":
            argList[i - 1] = argList[i - 1] + "_"
            del argList[i]
            i -= 1
        elif i < len(argList) - 1 and argList[i] == "dash":
            argList[i] = "-" + argList[i + 1]
            del argList[i + 1]
        elif argList[i - 1].endswith(".") or argList[i - 1].endswith("_"):
            argList[i - 1] = argList[i - 1] + argList[i]
            del argList[i]
            i -= 1
        i += 1
            
    return argList

def __extractOptions(args):
    options = {}
    i = 0
    while i < len(args):
        # Some dashed fields have special meanings.
        if args[i].startswith("-") and args[i] != "-or" and args[i] != "-and" and args[i] != "--or" and args[i] != "--and":
            if args[i].startswith("--"):
                if "=" in args[i]:
                    val = args[i][args[i].index("=") + 1:]
                    if re.sub('\.', '', val).isnumeric():
                        if '.' in val:
                            val = float(val)
                        else:
                            val = int(val)
                    options[args[i][2:args[i].index("=")]] = val
                else:
                    options[args[i][2:]] = True
            # These two have special meanings
            else:
                lastChar = None
                numBuilder = ''
                for char in args[i][1:]:
                    if char.isnumeric() or char == '.':
                        numBuilder += char
                    else:
                        if numBuilder:
                            if '.' in numBuilder:
                                options[lastChar] = float(numBuilder)
                            else:
                                options[lastChar] = int(numBuilder)
                            numBuilder = ''
                        lastChar = char
                        options[char] = True
                if lastChar and numBuilder:
                    options[lastChar] = float(numBuilder)
                    numBuilder = ''
            del args[i]
        elif args[i] == "playlist" or args[i] == "m3u":
            options["playlist"] = True
            del args[i]
        elif args[i].endswith(".m3u"):
            options["playlist"] = True
            args[i] = args[i][0:args[i].rindex(".m3u")]
            i += 1
        else:
            i += 1
    return options

'''
Compiles all arguments in the argument list into a SQLite search term

@param argList -    The SQL query array to add to.
@param args -       The search keywords
@param matchAll -   Designs the search query to match all arguments, not just
                    any argument.
@param playlist -   If true, then a playlist query is built.
@return A set of search keywords provided, stripped of all extra arguments and
        unused words (the, and, etc.)
'''
def __appendDatabaseArguments(argList, args, matchAll = False, playlist = False):
    # Common words that are in a lot of song titles that we should avoid
    commonWords = ["the", "off", "for", "from", "with", "and"]
    notArgs = []
    terms = set()
    if len(args) > 0:
        for arg in args:
            if arg.startswith("!"):
                notArgs.append(arg[1:])
            elif arg == "AND" or arg == "and" or arg == "-and" or arg =="--and" or arg == "&&":
                # Override whatever AND/OR we had before
                argList.pop()
                argList.append("AND")
            elif arg == "OR" or arg == "or" or arg == "-or" or arg =="--or" or arg == "||":
                # Override whatever AND/OR we had before
                argList.pop()
                argList.append("OR")
            elif len(arg) >= 3 and not arg in commonWords:
                argList.append("(")
                if playlist:
                    argList.append("playlists.name")
                    argList.append("LIKE")
                    argList.append("'%" + arg.replace("'", "''") + "%'")
                else:
                    argList.append("tracks.name")
                    argList.append("LIKE")
                    argList.append("'%" + arg.replace("'", "''") + "%'")
                    argList.append("OR")
                    argList.append("albums.name")
                    argList.append("LIKE")
                    argList.append("'%" + arg.replace("'", "''") + "%'")
                    argList.append("OR")
                    argList.append("artists.name")
                    argList.append("LIKE")
                    argList.append("'%" + arg.replace("'", "''") + "%'")
                argList.append(")")
                terms.add(arg)
                if matchAll:
                    argList.append("AND")
                else:
                    argList.append("OR")
        if argList[len(argList) - 1] == "AND" or argList[len(argList) - 1] == "OR":
            argList.pop()
        if len(notArgs) > 0:
            argList.append("AND")
            for arg in notArgs:
                argList.append("tracks.name")
                argList.append("NOT")
                argList.append("LIKE")
                argList.append("'%" + arg.replace("'", "''") + "%'")
                argList.append("AND")
            argList.pop()
    return terms

'''
Searches the databases for songs that match a series of provided keywords

@param terms -      A list of string options to match. If "playlist" is among
                    them, then playlist names will be added to the search
                    parameters.
@param matchRate -  The minimum percentage of terms that must be present in each
                    entry in order for it to be included in the results.
                    Defaults to 0.7
@param sortRandom - Whether nor not the entries should be randomized within
                    their match rates (i.e. two songs with a match rate of 2
                    terms each will be randomly inserted, but a song with a
                    match rate of 3 will always be after one with a rate of 2.)
                    Defaults to True.
@param playlist -   Whether or not to include playlists in the search. Defaults
                    to False.
@param database -   The path to the track database.
@param playlists -  The path to the playlist database.
@return A list of tuples, with each one containing whether or not the track was
        part of a playlist, a track URI, a lollypop track ID, an album name,
        and an artist name. The list is sorted with more relevent results
        appearing farther down the list.
'''
def searchDatabase(terms, matchRate = MATCH_RATE, matchAll = False, sortRandom = True, playlist = False, database = Path(Path.home(), ".local/share/lollypop/lollypop.db"), playlists = Path(Path.home(), ".local/share/lollypop/playlists.db")):
    files = []
    addedUris = []
    vals = []
    matchRate = MATCH_RATE
    
    db = sqlite3.connect(str(database))
    if playlist:
        dbPl = sqlite3.connect(str(playlists));
        findArgs = "SELECT tracks.uri, playlists.name FROM tracks INNER JOIN playlists ON tracks.playlist_id = playlists.id WHERE".split(" ")
        newTerms = __appendDatabaseArguments(findArgs, terms, matchAll = matchAll, playlist = True)
        songVals["terms"] = newTerms
        findArgs = " ".join(findArgs) + ";"
        results = dbPl.execute(findArgs);
        
        for row in results:
            matches = 0
            for term in newTerms:
                if term in re.sub('[^A-Za-z ]', '', row[1]).lower():
                    matches += 1
            if matches >= matchRate * len(newTerms):
                # Make playlist matches more important
                matches *= 10
                # Get the actual song data, as the playlist database o
                songResults = db.execute("SELECT tracks.uri, tracks.id, tracks.name FROM tracks INNER JOIN albums ON tracks.album_id = albums.id INNER JOIN track_artists ON tracks.id = track_artists.track_id INNER JOIN artists ON track_artists.artist_id = artists.id WHERE tracks.uri='%s' GROUP BY tracks.uri" % (row[0].replace("'", "''"))).fetchone()
                if songResults:
                    songVals[songResults[0]] = (matches, matches)
                    if sortRandom:
                        point = random.randint(bisect_left(vals, matches), bisect_right(vals, matches))
                    else:
                        point = bisect_right(vals, matches)
                    vals.insert(point, matches)
                    files.insert(point, (True,) + songResults)
                    addedUris.append(songResults[0])
        dbPl.close()
        
    # Focus on actual songs, now.
    findArgs = "SELECT tracks.uri, tracks.id, tracks.name, albums.name, artists.name FROM tracks INNER JOIN albums ON tracks.album_id = albums.id INNER JOIN track_artists ON tracks.id = track_artists.track_id INNER JOIN artists ON track_artists.artist_id = artists.id WHERE".split(" ")
    newTerms = __appendDatabaseArguments(findArgs, terms, matchAll = matchAll, playlist = False)
    findArgs.append("GROUP")
    findArgs.append("BY")
    findArgs.append("tracks.uri".replace("'", "''"))
    findArgs = " ".join(findArgs) + ";"
    #print(findArgs)
    results = db.execute(findArgs);
    
    for row in results:
        # Skip any songs added as part of a playlist
        if row[0] in addedUris:
            continue
        #print(row[1])
        row = (False,) + row
        val = getSongValue(row, newTerms)
        if val[0] >= matchRate * len(newTerms):
            # Inserts it in order, but random to matches of an equal stature
            if sortRandom:
                point = random.randint(bisect_left(vals, val[1]), bisect_right(vals, val[1]))
            else:
                point = bisect_right(vals, matches)
            vals.insert(point, val[1])
            files.insert(point, row)
    db.close()
    
    return files

'''
Plays a list of songs

@param files -      A list of songs as returned by searchDatabase. At minimum, each
                    element needs to be a tuple containing a boolean of whether or
                    not the song came from a playlist, the URI of the song file,
                    and the lollypop song ID.
@param separate -   Whether or not to launch the Lollypop process in a separate
                    process. Defaults to false (i.e. this process is replaced
                    with Lollypop
'''
def play(files, separate = False):
    for song in files:
        if song[1] in songVals:
            print("%02d - %s" % (songVals[song[1]][0], song[1]))
        else:
            print("Pl - %s" % (song[1]))
    ids = []
    for i in range(len(files)):
        ids.append("t:%s" % (files[i][2]))
        files[i] = files[i][1]

    vlcArgs = ["lollypop"]
    vlcArgs.append("-a")
    vlcArgs.append(";".join(ids))
    #print(" ".join(vlcArgs))
    print("Launching Lollypop: %s" % (vlcArgs))
    if separate:
        subprocess.Popen(vlcArgs)
    else:
        os.execvp(vlcArgs[0], vlcArgs)

def __main__():
    # Checks if Lollypop is installed
    missing = subprocess.call("command -v lollypop >> /dev/null", shell=True)
    if missing:
        print("Lollypop Music Player is not installed", file=sys.stderr)
        exit(1)
    
    __mergeWords(sys.argv)
    options = __extractOptions(sys.argv)
    if "h" in options or "help" in options:
        print("""Usage: %s [OPTIONS]... [TERM]...
Searches for a song within the music collection

OPTIONS:
-a                      The search must match every single term
-s                      Only the first option will play.
-h, --help              Shows this message
-m[rate], --match=<rate>All matches must have this percentage of matching
                        keywords in order to be included. Defaults to 0.65.

TERMS:
For the most part, you can just enter a single-word term, and it will be added
to the possible substrings included in the file name search. However, there are
a few additional ways to refine your search.

-and, --and, AND, and   Any of these keywords will cause the previous and next
                        terms to be linked together, so that they MUST appear
                        for the file to qualify.
-or, --or, OR, or       Any of these keywords will cause the previous and next
                        terms to be linked together, so that only one or the
                        other needs to appear for the file to qualify.
                        Overrides the -a option for those two terms.
!                       Add this to the beginning of a term to ensure that the
                        keyword does NOT appear in any matching file paths.
m3u, playlist           Normally, playlists are ignored during the file search.
                        However, this term will not only allow for their
                        search, but will also give them higher precedence.""" % (sys.argv[0]))
        exit(0)
        
    minAcceptance = MATCH_RATE
    if "match" in options:
        minAcceptance = options["match"]
    elif "m" in options:
        minAcceptance = options["m"]
    if minAcceptance > 10:
        minAcceptance /= 100
    elif minAcceptance > 1:
        minAcceptance /= 10
        
    files = searchDatabase(sys.argv[1:], matchRate = minAcceptance, matchAll = "a" in options or "all" in options, playlist = "playlist" in options)
    
    if len(files) == 0:
        print("No files found", file=sys.stderr)
        exit(1)
    
    files.reverse()
    
    if "s" in options:
        files = [files[0]]

    play(files)
    exit(0)

if __name__ == "__main__":
    __main__()
