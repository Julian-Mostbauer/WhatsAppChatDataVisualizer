import re
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt

# ------------------------------- GLOBAL VARIABLES -------------------------------
message_pattern = re.compile(r"\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2} - (.*?): (.*)")
# message_pattern = re.compile(r"\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - (.*?): (.*)") # different locality
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

banned_words = ["<medien", "ausgeschlossen>", "lero", "<media", "omitted>", "this message was deleted"]

remove_emojis = True

group_name = "15BHIF"


# ------------------------------- GLOBAL VARIABLES -------------------------------

def main():
    messages = load_messages(f"Data/Collected/{group_name}.txt")
    [user_messages, general_result] = sort_messages(messages)

    word_frequencies = {}
    for user, msgs in user_messages.items():
        word_frequency = sort_frequency(get_word_frequency(msgs))
        word_frequencies[user] = word_frequency

    word_frequencies = {k: v for k, v in
                        sorted(word_frequencies.items(), key=lambda item: total_words(item[1]), reverse=True)}

    place_counter = 1
    for user, word_freq in word_frequencies.items():
        print(f"{place_counter}. User: {user}")
        print(f"Total words: {total_words(word_freq)}")
        print(f"Most common words: {word_freq}")
        print()
        place_counter += 1

    # most used words from all users combined
    general_frequencies = sort_frequency(get_word_frequency(general_result["General"]))
    print(general_frequencies[:10])

    # Data for plotting
    labels = word_frequencies.keys()
    sizes = [total_words(word_freq) for word_freq in word_frequencies.values()]
    explode = [0.2 if size == max(sizes) else 0.1 for size in sizes]

    # Plot
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig(f"Data/Generated/{group_name}.png")
    plt.show()

    plt.close()


def load_messages(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        return file.readlines()


def total_words(word_freq):
    return sum([x[1] for x in word_freq])


def get_word_frequency(messages):
    word_frequency = {}
    for message in messages:
        words = message.split(" ")
        for word in words:
            word = word.lower()
            if word:
                if word in word_frequency:
                    word_frequency[word] += 1
                else:
                    word_frequency[word] = 1
    return word_frequency


def sort_frequency(frequency) -> [[str, int]]:
    return sorted(frequency.items(), key=lambda x: x[1], reverse=True)


def sort_messages(messages) -> [dict]:
    general_messages = defaultdict(list)
    user_messages = defaultdict(list)

    for message in messages:
        match = message_pattern.match(message)
        if match:
            user = match.group(1).strip()
            msg = match.group(2).strip().lower()

            for banned_word in banned_words:
                msg = msg.replace(banned_word, "")

            msg = msg.strip()
            if msg:
                if remove_emojis:
                    msg = emoji_pattern.sub(r'', msg)
                user_messages[user].append(msg)
                general_messages["General"].append(msg)

    return [user_messages, general_messages]


if __name__ == '__main__':
    main()
