# AkinatorBot(ALPHA VERSION)
 A majestic hello, my friends! This is a copy of the famous game "Akinator". Your objective - mind your character, I'll guess your character or not:)

**Link on my video-showing**

[![Google Drive](https://img.shields.io/badge/Google_Drive-4285F4?style=for-the-badge&logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1HZzzaCebGiXYlAky8xmzNcEJ9arxcp0z/view?usp=drive_link)

## Game's features:
1. Language of the game is only 󠁧󠁢**English**.
2. This TelegramBot guesses Marvel superheroes (includes **20743** characters).
3. It's tracking **your wins** and **Akinator's wins**.
4. You'll always be the first to know about **upcoming versions**.
## Game Mechanics:
1. A player gets a request from Akinator.
2. A received response from an user.
3. Akinator counts **probability percentages(%)** of characters.
## Tech Stack:

1. Program language is **Python 3.11**.
2. The AI model ''**openai/gpt-oss-20b**'' has used in this project from **groq**.
3. Databases: **SQLite3**.
4. Framework: **telebot**
5. ''rag'': chromadb.
6. Data Processing: pandas
## Project Structure:

`rag.py` -  the main file for Akinator.

`TelegramAkinator_Alpha.py` - this file handles for TelegramBot interface.

`marvel_characters_database1.csv` - the database of all Marvel superheroes.

`IDs.py` - the file of functions for interacting with database.

## Functions for TelegramBot interface:
|Sector|Function/Command|Description|
|:--:|:---:|:---|
|Primary|`/start`|registration or restart the bot|
|Primary|`/answers`|how need to answer questions|
|Primary|`/play`|it's definitely play|
|Secondary|`/statistics`|your wins and Akinator's wins|
|Secondary|`/help`|how to play this game|
|Secondary|`/extra`|extra information about Akinator's system|
|Tertiary|`/creators`|people who made Akinator|
|Tertiary|`/updates`|information about previous and current versions of this game|

## Installation:
1. Install repository: "https://github.com/leshkakozlovski-boop/AkinatorBot-Alpha-"
2. Write in terminal 👇
``` bash
pip install -r requirements.txt
```

## Database Schema:
**messages**

|Name|Type|Function|
|:--:|:---:|:---|
|id|integer|a number of a message|
|user_id|integer|a number of a user|
|positive_answers|str|positive facts about user's character|
|known_facts|str|all fact about user's character|

**sessions**
|Name|Type|Function|
|:--:|:---:|:---|
|user_id|integer|a number of a user|
|actual_question_number|integer|current number of a question|
|akinator_wins|integer|Akinator's wins|
|user_wins|integer|user's wins|
|last_question|str|last question from Akinator|
|is_final_state|integer|Is it final question or not|


## RoadMap:
In next **upcoming versions** i'll:
1. Add another languages, like: **Russian**, **Spanish**, **Serbian**, **Chinese**, **German**.

2. Add **store** of your wins(???).

3. Add **leaderboard**.

   

   thank you for reading of my readme! good luck for testing Akinator :)