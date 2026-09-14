import os
import chromadb
import pandas as pd
from openai import OpenAI
from IDs import positive_answers_select, save_messages_positive, save_messages_known_facts, known_facts_select, \
    get_session, update_session

chroma_client = chromadb.PersistentClient(path="./akinator.db")
collection = chroma_client.get_or_create_collection(name="akinator_char")

actual_question_number=0
akinator_wins=0
user_wins=0

if collection.count() == 0:
    csv_file = "marvel_characters_database1.csv"
    if os.path.exists(csv_file):
        print(f"[Система] Читаем файл {csv_file}...")

        column_names = [
            "Name", "Gender", "Eye Color", "Hair Color", "Superpowers", "Weakness", "Alignment",
            "Status", "Identity", "Race", "Skin Color", "Can_Fly", "Has_Claws", "Healing_Factor",
            "Uses_Magic", "Wears_Armor", "Super_Strength", "Telepathy", "Super_Speed", "Shoots_Webs",
            "Vulnerable_to_Magic", "Vulnerable_to_Physical", "Vulnerable_to_Energy", "Is_Marvel",
            "Is_DC", "Is_X_Men", "Is_Avenger", "Is_Batman_Family", "Is_Spider_Man_Family",
            "Is_Fantastic_Four"
        ]
        df = pd.read_csv(csv_file, header=None, names=column_names)

        documents = []
        metadatas = []
        ids = []

        print(len(df))

        for idx, row in df.iterrows():
            valid_data = row.dropna()
            desc_parts = []
            for col, val in valid_data.items():
                if col != "Name":
                    desc_parts.append(f"{col}: {str(val).strip()}")

            desc_text = "; ".join(desc_parts)
            char_name = str(row["Name"]).strip()

            documents.append(desc_text)
            metadatas.append({"Name": char_name})
            ids.append(f"char_{idx}")

        print("Начинаем загрузку векторов в базу (партиями по 250)")
        batch_size = 250
        for i in range(0, len(documents), batch_size):
            collection.add(
                documents=documents[i: i + batch_size],
                metadatas=metadatas[i: i + batch_size],
                ids=ids[i: i + batch_size]
            )
            print(f"Загружено {min(i + batch_size, len(documents))} / {len(documents)}")

        print("База данных успешно сформирована!\n")
    else:
        print(f"[Ошибка] Файл {csv_file} не найден!")
        exit(1)

client = OpenAI(
    api_key="key",
    base_url="https://api.groq.com/openai/v1"
)

def play(user_id, user_answer=None):
    session = get_session(user_id)
    positive_answers = positive_answers_select(user_id)
    known_facts = known_facts_select(user_id)
    positive_answers = [ans[0] for ans in positive_answers if ans]
    known_facts = [fact[0] for fact in known_facts if fact]
    if user_answer is not None:
        user_answer = str(user_answer).lower().strip()
        if user_answer in ["ye", "yeah", "yep", "yes", "да", "da", "y", "д"]:
            user_answer = "yes"
        elif user_answer in ["prob", "probabl", "prbl", "probab", "вероятно", "veroyatno", "p", "в"]:
            user_answer = "probably"
        elif user_answer in ["no", "nope", "nah", "ne", "na", "not", "нет", "net", "ni", "neh", "n", "н"]:
            user_answer = "no"
        elif user_answer in ["not sr", "ntsr", "not sur", "не уверен", "ne uveren", "hoty glaza vikoli", "ns","i don't know", "idk", "i dont know", "ну"]:
            user_answer = "not sure"

    if session["last_question"] and user_answer:
        known_facts.append(f"Q: {session['last_question']} -> A: {user_answer}")
        save_messages_known_facts(user_id, session["last_question"], user_answer)
        if user_answer in ["yes", "probably"]:
            keywords = session["last_question"].replace("Final question: Is this", "").replace("Does the character", "").replace(
                "Does he", "").replace("Does she", "").replace("Is the character", "").strip("? ")
            positive_answers.append(keywords)
            save_messages_positive(user_id, keywords)

        if session["is_final_state"]:
            if user_answer in ["yes", "probably"]:
                session["akinator_wins"] += 1
                update_session(user_id,0, session["akinator_wins"], session["user_wins"], "", False)
                msg = f"Ура! Я угадал! \n(Счет: Акинатор {session['akinator_wins']} - Игрок {session['user_wins']})"
                print(msg)
                return msg
            else:
                session["user_wins"] += 1
                update_session(user_id, 0, session["akinator_wins"], session["user_wins"], "", False)
                msg = f"Жаль, я не угадал. Давай сыграем еще раз! \n(Счет: Акинатор {session['akinator_wins']} - Игрок {session['user_wins']})"
                print(msg)
                return msg

    if len(positive_answers) > 0:
        positive_answers1=[]
        for i in positive_answers:

            if i is not None:
                positive_answers.append(i)
        search = " ".join(positive_answers1)
    else:
        search = "marvel character superhero human"


    results = collection.query(
        query_texts=[search],
        n_results=10
    )

    rag_content = ""
    if results['documents'] and results['documents'][0]:
        for i in range(len(results['documents'][0])):
            name = results['metadatas'][0][i]['Name']
            desc = results['documents'][0][i]
            rag_content += f"- {name}: {desc}\n"

    prompt = f'''
    You have this information which user has approved and rejected: {known_facts}
    And your database about characters which match these traits:
    {rag_content}

    Your objective is to guess a character. The user can respond with: yes, no, probably, not sure.
    INSTRUCTIONS:
    - +1.1. You must ask a player only about the Marvel characters.
    - +1.2. Based on their answers, find matching descriptions. Ask a question to eliminate candidates.
    - +2.1. Create ONLY closed questions (yes/no).
    - +2.2. If you have guessed correctly or are sure, write exactly: "Final question: Is this [Name]?".
    - +2.3. Output exactly one question.
    - +2.4. You mustn't ask a user; Is the person a trans man?".
    - +3.1. Output ONLY the question itself. No introductory text, no thoughts.
    - +3.2.  You have the access to data: "Name", "Gender", "Eye Color", "Hair Color", "Superpowers", "Weakness", "Alignment",
            "Status", "Identity", "Race", "Skin Color", "Can_Fly", "Has_Claws", "Healing_Factor",
            "Uses_Magic", "Wears_Armor", "Super_Strength", "Telepathy", "Super_Speed", "Shoots_Webs",
            "Vulnerable_to_Magic", "Vulnerable_to_Physical", "Vulnerable_to_Energy", "Is_Marvel",
            "Is_DC", "Is_X_Men", "Is_Avenger", "Is_Batman_Family", "Is_Spider_Man_Family",
            "Is_Fantastic_Four"
    - +3.3. Think wisely, like: if user has answered: person isn't female, definitely it's male!!
    '''
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.55
    )
    clean_question = response.choices[0].message.content
    # clean_question = re.sub(r'<think>.*?</think>', '', ai_reply, flags=re.DOTALL).strip()
    session["last_question"] = clean_question
    print("a\n")
    session["actual_question_number"] +=1
    session["is_final_state"]= "Final question:" in clean_question
    update_session(user_id, session["actual_question_number"], session["akinator_wins"], session["user_wins"], session["last_question"], session["is_final_state"])
    return f"{session['actual_question_number']}, {clean_question}"