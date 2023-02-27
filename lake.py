from intent import Intent
class Lake:
    def __init__(self, intentMap={}, intex=""):
        self.name = ""
        self.map = intentMap  # full lake
        self.val = {}  # validation set
        self.allutter = []
        self.outlst = []
        self.allheaders = []  # header of every intent in lake

        if intex:
            self.addLakeFromFile(intex)
            self.gatherUtterances()

    def __str__(self):
        strFull = ""
        allheadersStr = '\n'.join(self.allheaders)
        strFull += allheadersStr
        for intentName in self.map:
            intent = self.map[intentName]
            strFull += intent.printOut()
        return strFull

    # imports an entire Intent Export as a lake
    # currently every intent MUST have a header
    def addLakeFromFile(self, intex):
        with open(intex, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                splt = line.split("\t")

                # check for header lines and create new intent for it
                if splt[0] == "#":
                    name = splt[1]
                    newIntent = Intent(name)
                    newIntent.header = line
                    # add header to lake as well
                    self.allheaders.append(line)
                    self.map[name] = newIntent
                # otherwise it is an utterance line
                else:
                    name = splt[0]
                    utterance = splt[1]

                    # all intents should exist at this point (see above) so no need to check
                    # if name in self.map:
                    #     self.map[name].addUtterance(utterance)
                    # else:
                    newIntent = Intent(name)
                    newIntent.addUtterance(utterance)
                    self.map[name] = newIntent

            # set headers for lake for easy output

            return self.map

    def gatherUtterances(self):
        for intent in self.map:
            for key in self.map[intent].utterances:
                self.allutter.append((intent, self.map[intent].utterances[key]))

        return self.allutter

    def getPercentageOfUtterances(self, n):
        n = float(n)
        with open("outfile.tsv", "w", encoding="utf-8") as of:
            for intent in self.map:
                intentObj = self.map[intent]
                of.write(intentObj.getPercentageOfUtterances(n))
        return

    def printOutLake(self, outfn):
        allheadersStr = '\n'.join(self.allheaders)
        with open(outfn, "w", encoding="utf-8") as of:
            of.write(allheadersStr)
            for intentName in self.map:
                intent = self.map[intentName]
                of.write(intent.printOut())

    def compare(self, lake):
        #for intentNameMine in self.map:
        return

    def splitAndPrintValidation(self, n=0.2):
        n = float(n)
        with open("lakeOutput.tsv", "a", encoding="utf-8") as mf:
            with open("lakeValidation.tsv", "a", encoding="utf-8") as valf:
                for intentName in self.map:
                    intent = self.map[intentName]
                    if len(intent.utterances) > 3:
                        intent.splitValidation(n)
                        tup = intent.printOut(val=True)
                        mf.write(tup[0])
                        valf.write(tup[1])
                    else:
                        mf.write(intent.printOut())
        return

    # update the lake fields when stuff gets added
    def updateLake(self):
        return