class Lake:
    def __init__(self, intentMap):
        self.name = ""
        self.map = intentMap # full lake
        self.val = {} # validation set
        self.allutter = []
        self.outlst = []

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
        with open(outfn, "w", encoding="utf-8") as of:
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