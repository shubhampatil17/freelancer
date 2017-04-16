import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


class PlacementPredictor:

    dataframe = pd.read_excel('training.xlsx', header=0)
    sslc_percentage_encoder = LabelEncoder()
    hsc_percentage_encoder = LabelEncoder()
    cgpa_encoder = LabelEncoder()
    class_encoder = LabelEncoder()

    # classifier = MultinomialNB()
    classifier = LogisticRegression()

    def __init__(self):
        print("Initializing training data ...", end='')
        self.dataframe = self.dataframe.fillna(0)

        self.sslc_percentage_encoder.fit(self.dataframe['SSLC Percentage'].values.tolist())
        self.hsc_percentage_encoder.fit(self.dataframe['HSC Percentage'].values.tolist())
        self.cgpa_encoder.fit(self.dataframe['Cgpa'].values.tolist())
        self.class_encoder.fit(self.dataframe['class'].values.tolist())

        self.dataframe['SSLC Percentage'] = self.sslc_percentage_encoder.transform(self.dataframe['SSLC Percentage'].values.tolist())
        self.dataframe['HSC Percentage'] = self.hsc_percentage_encoder.transform(self.dataframe['HSC Percentage'].values.tolist())
        self.dataframe['Cgpa'] = self.cgpa_encoder.transform(self.dataframe['Cgpa'].values.tolist())

        features_matrix = self.dataframe[self.dataframe.columns[:-1]].values
        response_vector = self.class_encoder.transform(self.dataframe[self.dataframe.columns[-1]].values.tolist())
        print("DONE.")

        print("Training Machine Learning Model ...", end='')
        self.classifier.fit(features_matrix, response_vector)
        print("DONE.")

    def update_encoder(self, encoder, sample):
        if sample not in encoder.classes_.tolist():
            encoder.fit(encoder.classes_.tolist() + [sample])

    def get_placement_probability(self, sslc_percentage, hsc_percentage, cgpa, intern, projects, languages, tools):
        sample = [sslc_percentage, hsc_percentage, cgpa, intern, projects, languages, tools]
        sample = [x if x else 0 for x in sample]

        self.update_encoder(self.sslc_percentage_encoder, sample[0])
        self.update_encoder(self.hsc_percentage_encoder, sample[1])
        self.update_encoder(self.cgpa_encoder, sample[2])

        sample[0] = self.sslc_percentage_encoder.transform([sample[0]])[0]
        sample[1] = self.hsc_percentage_encoder.transform([sample[1]])[0]
        sample[2] = self.cgpa_encoder.transform([sample[2]])[0]
        sample[3] = int(sample[3])
        sample[4] = int(sample[4])
        sample[5] = int(sample[5])
        sample[6] = int(sample[6])

        class_labels = self.classifier.predict([sample])
        probability = self.classifier.predict_proba([sample])
        return probability[0][1]*100


if __name__ == "__main__":

    predictor = PlacementPredictor()

    cont = "y"
    while cont == "y":
        print("\nEnter a new sample ... ")

        sslc_percentage = input("SSLC Percentage :")
        hsc_percentage = input("HSC Percentage :")
        cgpa = input("Cgpa :")
        intern = input("Intern :")
        projects = input("Projects :")
        languages = input("Languages :")
        tools = input("Software Tools :")

        probability = predictor.get_placement_probability(
            sslc_percentage=sslc_percentage,
            hsc_percentage=hsc_percentage,
            cgpa=cgpa,
            intern=intern,
            projects=projects,
            languages=languages,
            tools=tools
        )

        print("\nProbability of placement for this sample is {}%".format(probability))
        cont = input("\nEnter 'y' to continue :")