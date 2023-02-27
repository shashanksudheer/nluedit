class Intent:
    def __init__(self, name=""):
        self.name = name
        self.utterances = {}
        self.utterCount = 0
        self.utterancePrediction = {}
        self.validation = [] # id's of utterances used for validation

    # Function to output string versions of the utterances
    # INPUT
    #       val - bool config option that determines whether to output just the intent utterances
    #             as a whole, or whether to output as a split of validation and the rest
    # OUTPUT
    #       string - A String of all the utterances with standard TSV formatting (INTENT\tUTTERANCE)
    #                or a tuple with two strings: string[0]: normal utterances | string[1]: validation
    def printOut(self, val=False):
        string = ""
        if not val:
            for i in range(0, len(self.utterances.values())):
                string += self.name + "\t" + list(self.utterances.values())[i]
                if i < len(self.utterances.values()):
                    string += "\n"

            return string
        else:
            stringVal = ""
            for i in range(0, len(self.utterances.values())):
                if i not in self.validation:
                    string += self.name + "\t" + list(self.utterances.values())[i]
                    if i < len(self.utterances.values()):
                        string += "\n"
                else:
                    stringVal += self.name + "\t" + list(self.utterances.values())[i]
                    if i < len(self.utterances.values()):
                        stringVal += "\n"

            tup = (string, stringVal)
            return tup

    # if the file contains predictions set predictFlag to true and pass in a prediction
    def addUtterance(self, utter, predictFlag=False, predictIntent="prediction"):
        if predictFlag:
            self.utterances[self.utterCount] = utter
            self.utterancePrediction[self.utterCount] = predictIntent
            self.utterCount += 1
        else:
            self.utterances[self.utterCount] = utter
            self.utterCount += 1

    def getPercentageOfUtterances(self, n):
        utterCt = int(len(self.utterances) * n) + 1
        utterLst = list(self.utterances.values())
        string = ""
        for i in range(utterCt):
            string += self.name + "\t" + utterLst[i] + "\n"
        # splice out \n character at the end
        string = string[:-1]
        return string

    def splitValidation(self, n=0.2):
        keyLst = list(self.utterances.keys())
        step = int(len(keyLst) / (len(keyLst) * n))

        for i in range(0, len(keyLst), step):
            self.validation.append(keyLst[i])

        return

    def __str__(self):
        string = self.printOut()
        return string
