import csv
import json
 
def csv_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.DictReader(file_obj)
    formatted = []
    for row in reader:
        if (row["reviews.rating"] == "5" or row["reviews.rating"] == "1"):
            formatted.append([row["reviews.text"], row["reviews.rating"]])
    for i in range(int(len(formatted)/10), len(formatted)):
        formatted[i][1] = ''

    jsonData = []
    for r in formatted:
        new_r = {}
        new_r['text'] = r[0]
        if (len(r[1])):
            new_r['label'] = r[1]
        jsonData.append(new_r)
    with open('hotels_data.csv', 'w') as outfile:
        for js in jsonData:
            outfile.write("\"" + js['text'].replace('"', '\\"') + '\"\n')

    with open('hotels_labels.csv', 'w') as outfile:
        outfile.write('text,label\n')
        for js in jsonData:
            if (js.get('label')):
                outfile.write("\"" + js['text'].replace('"', '\\"') + '\",\"' + js['label'] + '\"\n')

 
if __name__ == "__main__":
    csv_path = "hotel_reviews.csv"
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)