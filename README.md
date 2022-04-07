<!-- PROJECT SHIELDS -->
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/jaredfiacco2/ClashOfClans_API">
    <img src="images/coc.png" alt="Logo" width="120" height="75">
  </a>

  <h3 align="center">Clash of Clans API - Automatically ETL, Store, Report Data with GCP</h3>

  <p align="center">
    This python code uses python to get Clash of Clans statistics on a schedule, using Cloud Scheduler, BigQuery using Pub/Sub and Cloud Functions, Virtual Private Cloud, Cloud Nat, Cloud Router, and Data Studio.
    <br />
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#prerequisites">Prerequisites & Instructions</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

- This project gives functions the user can use to pull data about fact data like clans, players, war logs, global rankings, and dimension data like locations, player labels, clan labels, leauges, etc. (Backend API Code in "apiHelper.py", get response in df form using "main.py" functions)

- This project, also was deployed entirely in GCP. It uses Cloud Scheduler and Pub/Sub to trigger a Cloud Functions 2x daily. This Cloud Function runs Python code that pulls data from Clash of Clans API through a static API provided by the Virtual Private Cloud, Cloud NAT & Cloud Router. The API data is stored in BigQuery and served as a Data Studio report emailed daily.

- Note: There is a small cost to running the VPC/NAT/Router combo. It's the only way to get a static IP egress needed for the Clash of Clans API call. My estimates are ~$13/month. Depending on how many clans you lead, how serious of a player you are,and if you use the VPC for another project, it might be worth the investment.

<img src="images\Cloud_functions_api_architecture.png" alt="Process Map"/>

### Built With

* [Python](https://python.org)
* [Cloud Scheduler](https://cloud.google.com/)
* [Pub/Sub](https://cloud.google.com/pubsub)
* [Cloud Functions](https://cloud.google.com/functions)
* [Virtual Private Cloud](https://cloud.google.com/vpc)
* [Cloud NAT](https://cloud.google.com/nat)
* [Cloud Router](https://cloud.google.com/network-connectivity/docs/router)
* [BigQuery](https://cloud.google.com/bigquery)
* [Data Studio](https://datastudio.google.com/)
* [Clash of Clans API](https://developer.clashofclans.com/#/)

### Prerequisites & Instructions

1. Installing all Required Packages
  ```sh
  pip install -r requirements.txt
  ```

2. Open a Google Cloud Platform Account and create a new project. 

3. Open the IAM & Admin page, set up permissions and obtain an API key. Replace this key with the \CloudFunction ".json" key.
<img src="images\IAM_Admin.png" alt="set up permissions" />

4. Ensure a default Virtual Private Cloud exists in GCP.
<img src="images\create_vpc.png" alt="set up cloud fucntions" />

5. Create a Serverless VPC Access Connector in GCP.
<img src="images\create_serverless_vpc_access_connector.png" alt="set up serverless vpc access connector" />

6. Create a Cloud Router in GCP.
<img src="images\create_cloud_router.png" alt="set up cloud router" />

7. Create a Cloud NAT in GCP.
<img src="images\create_cloud_nat.png" alt="set up cloud nat" />

8. Create a SuperCell account, and [Create an API Key](https://developer.clashofclans.com/#/new-key) to access Clash of Clans data. Use the Static IP Address from the NAT Gateway Step. Plug this into the cloud functions main.py as the API_KEY. Make another with your home IP Adress if you want to test locally.
<img src="images\coc-api-create-key.png" alt="set up permissions" />

9. Set up a Pub/Sub Topic.
<img src="images\create_pub_sub_topic.png" alt="create generic pub/sub topic" />

10. Set up a Cloud Scheduler to send the Pub/Sub topic trigger to Cloud Functions 2x daily.
<img src="images\create_cloud_scheduler.png" alt="set up cloud scheduler to trigger cloud function through pub/sub" />

11. Set up the Cloud Function with the following trigger, code, and connection settings.
* Trigger Settings
    <img src="images\create_cloud_function_pub_sub.png" alt="set up cloud fucntions" />
* Code Settings
    <img src="images\create_cloud_function_code.png" alt="set up cloud fucntions" />
* Connection Settings
    <img src="images\create_cloud_function_connection.png" alt="set up cloud fucntions" />

12. Use BigQuery to check query your computers' stats over time.
<img src="images\BigQuery.png" alt="use BigQuery to query the stats" />

13. Create a [Data Studio Report](https://datastudio.google.com/reporting/0a950cb7-3b1d-4bd5-b467-da6d7b7a1183) connecting to BigQuery. Set report to send daily via email.
<img src="images\DataStudio.png" alt="use BigQuery to query the stats" />

14. Test locally and adjust the cloud function python script by using the apiHelpers.py file and main.py file. Integrate customized functions into your automated ETL process!

<!-- CONTACT -->
## Contact

[Jared Fiacco](https://www.linkedin.com/in/jaredfiacco/) - jaredfiacco2@gmail.com

Another GCP Project of Mine: 
* [Transcribe Podcasts, Save to GCP Firebase](https://github.com/jaredfiacco2/FirebasePodcastTranscription)
* [Monitor & Store Computer Statistics in GCP BigQuery using Pub/Sub](https://github.com/jaredfiacco2/ComputerMonitoring_IOT)


This project was inspired by:
* [GCP Cloud Functsions with a Static IP](https://dev.to/alvardev/gcp-cloud-functions-with-a-static-ip-3fe9)
* [How to create a Firebase Cloud Function with static outbound IP](https://medium.com/@scorpion.nimit/how-to-create-a-firebase-cloud-function-with-static-outbound-ip-8086bbbdbbfe#:~:text=To%20have%20a%20static%20outbound%20IP%2C%20you%20need%20to%20connect,function%20to%20a%20VPC%20Connector)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jaredfiacco/