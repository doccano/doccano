import Vue from 'vue';
import annotationMixin from './demo_mixin';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],
  data: {
    docs: [{
      id: 1,
      text: 'Fair drama/love story movie that focuses on the lives of blue collar people finding new life thru new love.The acting here is good but the film fails in cinematography,screenplay,directing and editing.The story/script is only average at best.This film will be enjoyed by Fonda and De Niro fans and by people who love middle age love stories where in the coartship is on a more wiser and cautious level.It would also be interesting for people who are interested on the subject matter regarding illiteracy.......',
    },
    {
      id: 10,
      text: "If you like adult comedy cartoons, like South Park, then this is nearly a similar format about the small adventures of three teenage girls at Bromwell High. Keisha, Natella and Latrina have given exploding sweets and behaved like bitches, I think Keisha is a good leader. There are also small stories going on with the teachers of the school. There's the idiotic principal, Mr. Bip, the nervous Maths teacher and many others. The cast is also fantastic, Lenny Henry's Gina Yashere, EastEnders Chrissie Watts, Tracy-Ann Oberman, Smack The Pony's Doon Mackichan, Dead Ringers' Mark Perry and Blunder's Nina Conti. I didn't know this came from Canada, but it is very good. Very good!",
    },
    {
      id: 11,
      text: "I came in in the middle of this film so I had no idea about any credits or even its title till I looked it up here, where I see that it has received a mixed reception by your commentators. I'm on the positive side regarding this film but one thing really caught my attention as I watched: the beautiful and sensitive score written in a Coplandesque Americana style. My surprise was great when I discovered the score to have been written by none other than John Williams himself. True he has written sensitive and poignant scores such as Schindler's List but one usually associates his name with such bombasticities as Star Wars. But in my opinion what Williams has written for this movie surpasses anything I've ever heard of his for tenderness, sensitivity and beauty, fully in keeping with the tender and lovely plot of the movie. And another recent score of his, for Catch Me if You Can, shows still more wit and sophistication. As to Stanley and Iris, I like education movies like How Green was my Valley and Konrack, that one with John Voigt and his young African American charges in South Carolina, and Danny deVito's Renaissance Man, etc. They tell a necessary story of intellectual and spiritual awakening, a story which can't be told often enough. This one is an excellent addition to that genre.",
    },
    {
      id: 12,
      text: "Story of a man who has unnatural feelings for a pig. Starts out with a opening scene that is a terrific example of absurd comedy. A formal orchestra audience is turned into an insane, violent mob by the crazy chantings of it's singers. Unfortunately it stays absurd the WHOLE time with no general narrative eventually making it just too off putting. Even those from the era should be turned off. The cryptic dialogue would make Shakespeare seem easy to a third grader. On a technical level it's better than you might think with some good cinematography by future great Vilmos Zsigmond. Future stars Sally Kirkland and Frederic Forrest can be seen briefly.",
    },
    {
      id: 13,
      text: "Robert DeNiro plays the most unbelievably intelligent illiterate of all time. This movie is so wasteful of talent, it is truly disgusting. The script is unbelievable. The dialog is unbelievable. Jane Fonda's character is a caricature of herself, and not a funny one. The movie moves at a snail's pace, is photographed in an ill-advised manner, and is insufferably preachy. It also plugs in every cliche in the book. Swoozie Kurtz is excellent in a supporting role, but so what?<br /><br />Equally annoying is this new IMDB rule of requiring ten lines for every review. When a movie is this worthless, it doesn't require ten lines of text to let other readers know that it is a waste of time and tape. Avoid this movie.",
    },
    {
      id: 14,
      text: 'From the beginning of the movie, it gives the feeling the director is trying to portray something, what I mean to say that instead of the story dictating the style in which the movie should be made, he has gone in the opposite way, he had a type of move that he wanted to make, and wrote a story to suite it. And he has failed in it very badly. I guess he was trying to make a stylish movie. Any way I think this movie is a total waste of time and effort. In the credit of the director, he knows the media that he is working with, what I am trying to say is I have seen worst movies than this. Here at least the director knows to maintain the continuity in the movie. And the actors also have given a decent performance.',
    },
    ],
    labels: [
      {
        id: 1,
        text: 'Negative',
        shortcut: 'n',
        background_color: '#ff0033',
        text_color: '#ffffff',
      },
      {
        id: 2,
        text: 'Positive',
        shortcut: 'p',
        background_color: '#209cee',
        text_color: '#ffffff',
      },
    ],
    annotations: [
      [
        {
          id: 1,
          label: 2,
        },
      ],
      [],
      [],
      [],
      [],
      [],
    ],
  },

  methods: {
    isIn(label) {
      for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
        const a = this.annotations[this.pageNumber][i];
        if (a.label === label.id) {
          return a;
        }
      }
      return false;
    },

    addLabel(label) {
      const a = this.isIn(label);
      if (a) {
        this.removeLabel(a);
      } else {
        const annotation = {
          id: this.annotationId++,
          label: label.id,
        };
        this.annotations[this.pageNumber].push(annotation);
        console.log(this.annotations);
      }
    },
  },
});
