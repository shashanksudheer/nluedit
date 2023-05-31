import re
import csv

from intent import Intent
from lake import Lake

def addUtterancesFromFile(file, intentMap, opt="i"):
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            splt = line.split("\t")
            # first line should ALWAYS be what is "expected"
            name = splt[0]
            if opt == "i":
                utterance = splt[1]

                if name in intentMap:
                    intentMap[name].addUtterance(utterance)
                else:
                    newIntent = Intent(name)
                    newIntent.addUtterance(utterance)
                    intentMap[name] = newIntent
            elif opt == "p":
                prediction = splt[1]
                utterance = splt[2]

                if name in intentMap:
                    intentMap[name].addUtterance(utterance, True, prediction)
                else:
                    newIntent = Intent(name)
                    newIntent.addUtterance(utterance)
                    intentMap[name] = newIntent
            elif opt == "f":
                utterance = splt[3]

                if name in intentMap:
                    intentMap[name].addUtterance(utterance)
                else:
                    newIntent = Intent(name)
                    newIntent.addUtterance(utterance)
                    intentMap[name] = newIntent

        return intentMap

# function to map all utterances with what FallbackSearch entity value Amelia would predict
# PARAMS
#   fallback - FallbackSearch entity table tsv to test against
#   lake - The intent lake to test with
#   outputfn - filename to output results to
def outputFallbackMatches(fallback, lake, outputfn):
    with open(outputfn, "w+") as out:
        for utterance in lake.allutter:
            intentName = utterance[0]
            fallbackName = intentName
            utter = utterance[1]
            lowerUtter = utter.lower()

            # check for any matching items
            with open(fallback, "r") as fb:
                fbreader = csv.reader(fb, delimiter="\t")
                for line in fbreader:
                    if (line[0] == "Intent"):
                        continue
                    fbName = line[1]
                    regPatt = line[2]
                    if re.search(regPatt, lowerUtter) is not None:
                        fallbackName = fbName
                        # only match first fallback. Is this how it works in amelia?
                        break

            out.write(intentName + "\t" + fallbackName + "\t" + utter + "\n")

    return "All Done :)"

def mapDescriptions(old, new):
    oldMap = {}

    for i in old.allheaders:
        oldDesc = i.split("\t")[5]
        oldBPN = i.split("\t")[4]
        oldMap[oldBPN] = oldDesc

    for i in range(len(new.allheaders)):
        newHeader = new.allheaders[i].split("\t")
        newBPN = newHeader[4]

        if newBPN in oldMap:
            newHeader[5] = oldMap[newBPN]
            new.allheaders[i] = "\t".join(newHeader)

    return



def commitChanges(file, lake):
    #open(file, "w").close()
    #with open(file, "w", encoding="utf-8") as f:
    #    for line in file:
    return

def checkChanges(file, lake):

    return





if __name__ == '__main__':
    arch = "tf/intex.tsv"
    utteranceExport = "tf/intex2.tsv"
    outfile = "tf/outfile.tsv"
    # intentMap = {}
    # 3 line intent file (w/ prediction) add config option "p", otherwise "i" TODO: what is f?

    lake = Lake(intex=arch)
    perc = lake.percentageNoBPN(utteranceExport, default="intentDisambiguation")

    print(perc)

