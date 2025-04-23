import utils
import read_csv
import charts



def run():

    data = read_csv.read_csv('./Python102/app/data.csv')
    
    country = input('Escribe un país=>')
    country2 = country
    print(country2)
    result = utils.population_by_country(data,country)

    if len(result)>0:
        country = result[0]
        labels, values = utils.get_population(country)
        charts.generate_bar_chart(country2,labels,values)
        charts.generate_pie_chart(country2,labels,values)

if __name__ == '__main__':
    run()
    