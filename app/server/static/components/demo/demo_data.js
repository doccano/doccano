export const demoNamedEntity = {
  project: {
    guideline: '',
  },
  me: {
    is_superuser: false,
  },
  docs: [
    {
      id: 1,
      text: 'Barack Hussein Obama II (born August 4, 1961) is an American attorney and politician who served as the 44th President of the United States from January 20, 2009, to January 20, 2017. A member of the Democratic Party, he was the first African American to serve as president. He was previously a United States Senator from Illinois and a member of the Illinois State Senate.',
      annotations: [
        {
          id: 16,
          prob: 0.0,
          label: 1,
          start_offset: 0,
          end_offset: 23,
        },
        {
          id: 19,
          prob: 0.0,
          label: 2,
          start_offset: 121,
          end_offset: 138,
        },
        {
          id: 27,
          prob: 0.0,
          label: 2,
          start_offset: 321,
          end_offset: 329,
        },
        {
          id: 22,
          prob: 0.0,
          label: 3,
          start_offset: 199,
          end_offset: 215,
        },
        {
          id: 28,
          prob: 0.0,
          label: 3,
          start_offset: 350,
          end_offset: 371,
        },
        {
          id: 17,
          prob: 0.0,
          label: 5,
          start_offset: 30,
          end_offset: 44,
        },
        {
          id: 20,
          prob: 0.0,
          label: 5,
          start_offset: 144,
          end_offset: 160,
        },
        {
          id: 21,
          prob: 0.0,
          label: 5,
          start_offset: 165,
          end_offset: 181,
        },
        {
          id: 18,
          prob: 0.0,
          label: 6,
          start_offset: 52,
          end_offset: 60,
        },
        {
          id: 24,
          prob: 0.0,
          label: 6,
          start_offset: 234,
          end_offset: 250,
        },
        {
          id: 26,
          prob: 0.0,
          label: 6,
          start_offset: 294,
          end_offset: 315,
        },
      ],
    },
    {
      id: 10,
      text: 'The White House is the official residence and workplace of the President of the United States. It is located at 1600 Pennsylvania Avenue NW in Washington, D.C. and has been the residence of every U.S. President since John Adams in 1800. The term is often used as a metonym for the president and his advisers.',
      annotations: [],
    },
    {
      id: 11,
      text: "The Democratic Party is one of the two major contemporary political parties in the United States, along with the Republican Party. Tracing its heritage back to Thomas Jefferson and James Madison's Democratic-Republican Party, the modern-day Democratic Party was founded around 1828 by supporters of Andrew Jackson, making it the world's oldest active political party.",
      annotations: [],
    },
    {
      id: 12,
      text: "Stanford University (officially Leland Stanford Junior University, colloquially the Farm) is a private research university in Stanford, California. Stanford is known for its academic strength, wealth, proximity to Silicon Valley, and ranking as one of the world's top universities.",
      annotations: [],
    },
    {
      id: 13,
      text: 'Donald John Trump (born June 14, 1946) is the 45th and current President of the United States. Before entering politics, he was a businessman and television personality.',
      annotations: [],
    },
    {
      id: 14,
      text: "Silicon Valley (abbreviated as SV) is a region in the southern San Francisco Bay Area of Northern California, referring to the Santa Clara Valley, which serves as the global center for high technology, venture capital, innovation, and social media. San Jose is the Valley's largest city, the 3rd-largest in California, and the 10th-largest in the United States. Other major SV cities include Palo Alto, Santa Clara, Mountain View, and Sunnyvale. The San Jose Metropolitan Area has the third highest GDP per capita in the world (after Zurich, Switzerland and Oslo, Norway), according to the Brookings Institution.",
      annotations: [],
    },
  ],
  labels: [
    {
      id: 1,
      text: 'Person',
      suffix_key: 'p',
      background_color: '#209cee',
      text_color: '#ffffff',
    },
    {
      id: 2,
      text: 'Loc',
      suffix_key: 'l',
      background_color: '#ffcc00',
      text_color: '#333333',
    },
    {
      id: 3,
      text: 'Org',
      suffix_key: 'o',
      background_color: '#333333',
      text_color: '#ffffff',
    },
    {
      id: 4,
      text: 'Event',
      suffix_key: 'e',
      background_color: '#33cc99',
      text_color: '#ffffff',
    },
    {
      id: 5,
      text: 'Date',
      suffix_key: 'd',
      background_color: '#ff3333',
      text_color: '#ffffff',
    },
    {
      id: 6,
      text: 'Other',
      suffix_key: 'z',
      background_color: '#9933ff',
      text_color: '#ffffff',
    },
  ],
};

export const demoTextClassification = {
  me: {
    is_superuser: false,
  },
  project: {
    guideline: 'Insert text to provide labeling instructions to annotator here...',
  },
  docs: [
    {
      id: 1,
      text: 'Fair drama/love story movie that focuses on the lives of blue collar people finding new life thru new love.The acting here is good but the film fails in cinematography,screenplay,directing and editing.The story/script is only average at best.This film will be enjoyed by Fonda and De Niro fans and by people who love middle age love stories where in the coartship is on a more wiser and cautious level.It would also be interesting for people who are interested on the subject matter regarding illiteracy.......',
      annotations: [
        {
          id: 1,
          label: 2,
        },
      ],
    },
    {
      id: 10,
      text: "If you like adult comedy cartoons, like South Park, then this is nearly a similar format about the small adventures of three teenage girls at Bromwell High. Keisha, Natella and Latrina have given exploding sweets and behaved like bitches, I think Keisha is a good leader. There are also small stories going on with the teachers of the school. There's the idiotic principal, Mr. Bip, the nervous Maths teacher and many others. The cast is also fantastic, Lenny Henry's Gina Yashere, EastEnders Chrissie Watts, Tracy-Ann Oberman, Smack The Pony's Doon Mackichan, Dead Ringers' Mark Perry and Blunder's Nina Conti. I didn't know this came from Canada, but it is very good. Very good!",
      annotations: [],
    },
    {
      id: 11,
      text: "I came in in the middle of this film so I had no idea about any credits or even its title till I looked it up here, where I see that it has received a mixed reception by your commentators. I'm on the positive side regarding this film but one thing really caught my attention as I watched: the beautiful and sensitive score written in a Coplandesque Americana style. My surprise was great when I discovered the score to have been written by none other than John Williams himself. True he has written sensitive and poignant scores such as Schindler's List but one usually associates his name with such bombasticities as Star Wars. But in my opinion what Williams has written for this movie surpasses anything I've ever heard of his for tenderness, sensitivity and beauty, fully in keeping with the tender and lovely plot of the movie. And another recent score of his, for Catch Me if You Can, shows still more wit and sophistication. As to Stanley and Iris, I like education movies like How Green was my Valley and Konrack, that one with John Voigt and his young African American charges in South Carolina, and Danny deVito's Renaissance Man, etc. They tell a necessary story of intellectual and spiritual awakening, a story which can't be told often enough. This one is an excellent addition to that genre.",
      annotations: [],
    },
    {
      id: 12,
      text: "Story of a man who has unnatural feelings for a pig. Starts out with a opening scene that is a terrific example of absurd comedy. A formal orchestra audience is turned into an insane, violent mob by the crazy chantings of it's singers. Unfortunately it stays absurd the WHOLE time with no general narrative eventually making it just too off putting. Even those from the era should be turned off. The cryptic dialogue would make Shakespeare seem easy to a third grader. On a technical level it's better than you might think with some good cinematography by future great Vilmos Zsigmond. Future stars Sally Kirkland and Frederic Forrest can be seen briefly.",
      annotations: [],
    },
    {
      id: 13,
      text: "Robert DeNiro plays the most unbelievably intelligent illiterate of all time. This movie is so wasteful of talent, it is truly disgusting. The script is unbelievable. The dialog is unbelievable. Jane Fonda's character is a caricature of herself, and not a funny one. The movie moves at a snail's pace, is photographed in an ill-advised manner, and is insufferably preachy. It also plugs in every cliche in the book. Swoozie Kurtz is excellent in a supporting role, but so what?<br /><br />Equally annoying is this new IMDB rule of requiring ten lines for every review. When a movie is this worthless, it doesn't require ten lines of text to let other readers know that it is a waste of time and tape. Avoid this movie.",
      annotations: [],
    },
    {
      id: 14,
      text: 'From the beginning of the movie, it gives the feeling the director is trying to portray something, what I mean to say that instead of the story dictating the style in which the movie should be made, he has gone in the opposite way, he had a type of move that he wanted to make, and wrote a story to suite it. And he has failed in it very badly. I guess he was trying to make a stylish movie. Any way I think this movie is a total waste of time and effort. In the credit of the director, he knows the media that he is working with, what I am trying to say is I have seen worst movies than this. Here at least the director knows to maintain the continuity in the movie. And the actors also have given a decent performance.',
      annotations: [],
    },
  ],
  labels: [
    {
      id: 1,
      text: 'Negative',
      suffix_key: 'n',
      background_color: '#ff0033',
      text_color: '#ffffff',
    },
    {
      id: 2,
      text: 'Positive',
      suffix_key: 'p',
      background_color: '#209cee',
      text_color: '#ffffff',
    },
  ],
};

export const demoTranslation = {
  project: {
    guideline: '',
  },
  me: {
    is_superuser: false,
  },
  docs: [
    {
      id: 1,
      text: 'If it had not been for his help, I would have failed.',
      annotations: [
        {
          id: 1,
          text: "S'il ne m'avait pas aidé, j'aurais échoué.",
        },
        {
          id: 2,
          text: "S'il ne m'avait pas aidée, j'aurais échoué.",
        },
      ],
    },
    {
      id: 10,
      text: 'According to this magazine, my favorite actress will marry a jazz musician next spring.',
      annotations: [],
    },
    {
      id: 11,
      text: "It's not always possible to eat well when you are traveling in this part of the world.",
      annotations: [],
    },
    {
      id: 12,
      text: "It's still early. We should all just chill for a bit.",
      annotations: [],
    },
    {
      id: 13,
      text: "She got a master's degree three years ago.",
      annotations: [],
    },
    {
      id: 14,
      text: 'We adopted an alternative method.',
      annotations: [],
    },
  ],
};
