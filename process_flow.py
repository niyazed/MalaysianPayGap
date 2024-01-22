import os 
import easyocr
import datetime
import instaloader
from tqdm import tqdm
from metaflow import FlowSpec, Parameter, step, conda_base

# @conda_base(python="3.8.0", base=conda_base.DEFAULT_BASE)
class ProcessFlow(FlowSpec):
    iloader = instaloader.Instaloader(
        download_pictures=True,
        download_videos=False, 
        download_video_thumbnails=False,
        compress_json=False,
        save_metadata=False)
    start_date = Parameter("start_date", help="Define start date")
    end_date = Parameter("end_date", help="Define end date")
    profile = Parameter("profile", help="Define target instagram profile") 
    
    reader = easyocr.Reader(['en']) 
    @step
    def start(self):
        print(f"Start date: {self.start_date}")
        print(f"End date: {self.end_date}")
        print(f"Profile: {self.profile}")
        self.next(self.scrape_data)

    @step
    def scrape_data(self):
        print(f"Scraping profile {self.profile} for posts between {self.start_date} and {self.end_date}")
        since = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
        until = datetime.datetime.strptime(self.end_date, "%Y-%m-%d")
        
        posts = instaloader.Profile.from_username(self.iloader.context, self.profile).get_posts()
        filtered_posts = filter(lambda p: since <= p.date <= until, posts)
        for post in filtered_posts:
            self.iloader.download_post(post, self.profile)

        self.next(self.filter_data)
        
    @step
    def filter_data(self):
        print(f"Filtering out images only")
        for filename in os.listdir(self.profile):
            if not filename.endswith(".jpg"):
                os.remove(os.path.join(self.profile, filename))

        self.next(self.extract_text)
    @step
    def extract_text(self):
        print("Extracting text from images")
        self.text_container = []
        img_list = [os.path.join(self.profile, f) for f in os.listdir(self.profile) if f.endswith(".jpg")]
        for img in tqdm(img_list):
            result = self.reader.readtext(img, detail = 0)
            self.text_container.extend(result)
        self.next(self.save_data)
    @step
    def save_data(self):
        print("Saving data")
        with open(f'{self.profile}_data.txt', 'w') as f:
            f.write(" ".join(self.text_container))
            
        self.next(self.end)
    
    @step
    def end(self):
        print("End of Flow")


if __name__ == "__main__":
    ProcessFlow()
