# FYVE BOT

----
## What is FYVE BOT?

FYVE BOT is an education bot that strives to summarize a topic for the user. When the bot receives a topic, it searches through Bing and YouTube to find relevant information. For articles, FYVE BOT is able to summarize the text into a condensed and simpler version. For YouTube videos, the bot scrapes the page for a transcript before summarizing the information. Five choices of summaries and presented to the user in order to provide different analyses of the topic.

----
## Getting Started

Use the included make-file to build the project.

Run the following commands from the top-level directory:
    sudo make build
    make run 

----
## Usage

FYVE BOT can be run alone as well as added to other platforms such as GroupMe and Slack. The steps to use FYVE BOT are as follows:

1. Enter a topic.
2. Choose one of the five provided summaries of the topic.
3. Learn!

----
## Built With

* [Azure](https://azure.microsoft.com/en-us/) - cloud computing service for bot
* [Bing API](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/) - for finding relevant articles on a topic
* [YouTube API](https://developers.google.com/youtube/v3/) - for finding relevant videos on a topic
* [Selenium](https://www.seleniumhq.org/) - used to obtain the transcript of a YouTube video
* [Aylien API](https://aylien.com/text-api/summarization/) - summarizes long articles/transcripts
* [Deep Auto Punctuation](https://github.com/episodeyang/deep-auto-punctuation) - used to insert proper punctuation into a YouTube transcript

----
## Versioning

* 01/24/18 10:18AM FYVE BOT is resurrected
* 01/24/18 02:22AM FYVE BOT is terminated
* 01/24/18 00:48AM FYVE BOT is born

----
## Authors

* Samuel Bretz
* Nyle Malik
* Jonathon Murphy
* Mitchell Myers
* Gerardo Prada
* Eduardo Vargas

----
## License

MIT License


----
## Acknowledgements

@article{deeppunc,
  title={Deep-Auto-Punctuation},
  author={Yang, Ge},
  journal={arxiv},
  year={2017},
  doi={10.5281/zenodo.438358}
  url={https://zenodo.org/record/438358;
       https://github.com/episodeyang/deep-auto-punctuation}
}
