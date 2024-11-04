from bs4 import BeautifulSoup
import requests
import sqlite3


class _job:

    # counter to Stop while loop
    page = 0

    def __init__ (self):

        # make counter to count page with num function
        self.pages = 1

        # name of job you want search about in wuzzuf
        opearation = input("what is your job you want search about ... ?\n")

        # make loop to move on pages of search's result
        while True:

            pag = requests.get(f"https://wuzzuf.net/search/jobs/?a=2&q={opearation}&start={_job.page}")
            src = pag.content
            self.soup = BeautifulSoup(src, "lxml")

        # Make sure there are still pages
            if self.pages == _job.page:
                break

            else:

            # run all function 
                self.num()
                self.data_b()
                self.excute()
                
            # Increase the counter of loop
                _job.page+=1

    # connect database
    def data_b(self):

        self.con = sqlite3.connect("ob.db")
        self.cur = self.con.cursor()
        self.cur.execute("create table if not exists job(job text, company text, data_posted text, location text, link_job text , link_company text, requirements text)")
        self.con.commit()
        

    # scraping data from pages of wuzzuf 
    def excute(self):
        try :
            # all conianers of jobs
            self.header = self.soup.find_all("div", {"class":"css-pkv5jc"})

            # Ensure outputs are present
            if len(self.header) == 0 :
                print("no have data \n please write correct job ...\n") 

                # return run script 
                app = _job()


            else:
                # print counter of pages 
                print("loading page ", _job.page+1)
                
                # scraping container that's have infromation of job which you searched
                for div in self.header:

                    job = div.find("h2").text
                    company_name = div.find("div", {"class":"css-d7j1kk"}).find("a").text
                    link_job = div.find("h2").find("a").get("href")
                    link_company = div.find("div", {"class":"css-d7j1kk"}).find("a").get("href")

                    if link_company == None :
                        link_company = "unknown"

                    location = div.find("span",{"class":"css-5wys0k"}).text.strip()
                    date = div.find("div", {"class":"css-d7j1kk"}).find("div").text
                    req = div.find("div", {"class":"css-y4udm8"}).contents[1].get_text()

                # use function of save data in database and close database
                    self.save_db(job, company_name, date, location, link_job, link_company, req)
                self.con.close()

        except Exception as e :
            print(e)

    # save result in database
    def save_db(self,job, company, date,location_job, link_job, link_company, req):

        self.cur.execute("insert into job (job, company, data_posted, location, link_job, link_company, requirements) values(?,?,?,?,?,?,?)",(job, company, date, location_job, link_job, link_company, req))
        self.con.commit()

    # fuction to count pages of search's result
    def num(self):
        # search in page about number of result search
        number = self.soup.find("strong").get_text()
        pages = int(number)/15

        if pages != round(pages):
            self.pages = round(pages)+1


if __name__ == "__main__":
    app = _job()
    