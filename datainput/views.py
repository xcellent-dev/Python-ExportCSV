from django.shortcuts import render
from django.views.generic import TemplateView
from datainput.forms import UserInputData
import csv
from csv import writer
import random
import string
# Create your views here.


class HomeView(TemplateView):
    template_name = 'datainput/forminput.html'


    def get(self, request):
        form = UserInputData()
        return render(request, self.template_name, {'form':form})   


    def post(self, request):
        form = UserInputData(request.POST)
        if form.is_valid():
            firstPara = form.cleaned_data['stringLength']
            secondPara = form.cleaned_data['density']
            thridPara = form.cleaned_data['total_words']
            fourthPara = form.cleaned_data['main_keyword']
            fifthPara = form.cleaned_data['supporting_words']
            sixthPara = form.cleaned_data['supporting_density']
            seventhPara = form.cleaned_data['p_tags']

            # firstPara = 8
            # secondPara = 5
            # thridPara = 1300
            # fourthPara = "peluqueria burlada, peluqueria burgos, peluqueria toledo, peluqueria santander, peluqueria leon, peluqueria albacete, peluqueria terrassa, peluqueria ciudad real, peluqueria pamplona, peluqueria palencia, peluqueria estepona, peluqueria girona, peluqueria caceres, peluquería madrid, peluqueria logroño"
            fourthPara_list = list(fourthPara.split(",")) 
            #fifthPara = "corte,mujer,lavado,centro,peluquería,hombre,mapa,pelo,mostrar,tratamientos,peinado"
            fifthPara_list = list(fifthPara.split(",")) 
            # sixthPara = 0.3
            # seventhPara = 11

            filename="experimento_chorriclub"
            for e in range(10):
                keywords = fourthPara_list
                self.append_list_as_row(filename+str(e)+".csv",["title","body","keyword", "fake_key","random_sent"])
                for keyword in keywords:
                        result= self.random_page(secondPara, thridPara, keyword, fifthPara_list, sixthPara, seventhPara)
                        self.append_list_as_row(filename+str(e)+".csv",result)

            text = str(firstPara) + ' ' + str(secondPara) +' ' +str(thridPara) + ' ' + str(fourthPara)+ ' ' + str(fifthPara)+ ' ' + str(sixthPara)+ ' ' + str(seventhPara)
            with open('datainput/DataInput.csv', "a") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=form.cleaned_data.keys())
                writer.writerow(form.cleaned_data)
            form = UserInputData()

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)


    def randomString2(self, stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.sample(letters, stringLength))
   

    def random_page(self, density, total_words, main_keyword, supporting_words, supporting_density ,p_tags):

        number_keywords = total_words * density/100
        print("exact keyword", number_keywords)

        sup_total = supporting_density * int(len(supporting_words))
        print("sup total", sup_total)

        number_support = total_words * sup_total/100
        print("total support", number_support)

        total_words_fake =total_words - number_keywords - number_support
        print("total fake",total_words_fake)

        final_text = []
        for i in range(int(total_words_fake)):
            final_text.append(self.randomString2(8))
        #print(" ".join(final_text))
        print("len total", len(final_text))

        for ii in range(int(len(supporting_words))):
            for i in range(int(number_support)//len(supporting_words)):
                final_text.append(str(supporting_words[ii]))
        print("len total", len(final_text))

        for i in range(int(number_keywords)):
            final_text.append(main_keyword)
        print("len total", len(final_text))

        min_lenght_sentence = 4
        max_lenght_sentence = 10
        import random
        final_randomized_text = random.sample(final_text, len(final_text))

        print(len(final_randomized_text))

        print(len(final_text))
        #print(" ".join(final_randomized_text))
        starting_number = int(random.randint(min_lenght_sentence,max_lenght_sentence))
        print(starting_number)
        dots_position = []
        #print(total_words)
        while starting_number<total_words+len(dots_position)+1:
            random_numb = int(random.randint(4,8))
            starting_number+=random_numb+1
            #print(starting_number)
            dots_position.append(starting_number)
        capitalize_first = []
        for i in dots_position:
            capitalize_first.append(i+1)
            final_randomized_text.insert(i, '.')
        #print(capitalize_first)
        capitalize_first = capitalize_first[:1]
        print(len(final_randomized_text))

        final_text = " ".join(final_randomized_text)
        #print(final_text)
        from nltk.tokenize import sent_tokenize

        sentences = sent_tokenize(final_text)
        new_capitalized=[]
        for i in sentences:
            i = i.split(" ")        
            i[0]=i[0].capitalize()        
            new_capitalized.append(" ".join(i))
        #print(new_capitalized)
        #print(" ".join(new_capitalized))
        text_capitalized = " ".join(new_capitalized)

        text_capitalized = text_capitalized.replace(" .", ".")
        #print(text_capitalized)
        print("palabras totales",len(text_capitalized.split(" ")))
        text_sent = sent_tokenize(text_capitalized)
        #print(text_sent)
        len_sent= len(text_sent)
      
        n = len_sent//p_tags
        print("n", n)
        z = 0
        y = 0
        html_random=[]
        tags_position=[]
        while z<len_sent:
            z+=n
            if z > len_sent:
                z=len_sent
            tags_position.append(z)
        
        print(len_sent,tags_position)
        x = 0
        for i in tags_position:
            html_random.append("<p>")
            html_random.append(str("".join(text_sent[x:i])))
            html_random.append("</p>")

            x=i
        print("este es el final")
        final_output = "".join(html_random)
        final_output = final_output.replace(".", ". ")
        #print(final_output)
        title = []
        for i in range(5):
            title.append(self.randomString2(8).capitalize())
        title = " ".join(title)
        fake_key= self.randomString2(8)
        random_sent=[]
        for i in range(8):
            random_sent.append(self.randomString2(8))
        random_sent=" ".join(random_sent)
        return title,final_output, main_keyword,fake_key, random_sent


    def append_list_as_row(self, file_name, list_of_elem):
        # Open file in append mode
        with open(file_name, 'a+', newline='', encoding="utf-8") as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)