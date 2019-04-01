import Vue from 'vue';
import annotationMixin from './mixin';
import HTTP from './http';

Vue.use(require('vue-shortkey'));

 

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
     wavesurfer: null,
     localStorage: {},
  },
  mixins: [annotationMixin],
  directives: {},

  updated () {
    this.$nextTick(() => {
      if (this.wavesurfer){
        this.wavesurfer.destroy(); // not destroy but remove regions and wave 
      }
      
      this.wavesurfer = WaveSurfer.create({
        container: '#waveform',
        height: 100,
        pixelRatio: 1,
        scrollParent: true,
        normalize: true,
        minimap: true,
        backend: 'MediaElement',
        plugins: [
            WaveSurfer.regions.create(),
            WaveSurfer.minimap.create({
                height: 30,
                waveColor: '#ddd',
                progressColor: '#999',
                cursorColor: '#999'
            }),
            WaveSurfer.timeline.create({
                container: '#wave-timeline'
            })
        ]
    });

    this.wavesurfer.load("/static/"+this.docs[this.pageNumber].text);
    this.addWaveSurfListeners();

    })
  },

  methods: {
    addWaveSurfListeners(){
      var me = this;


      this.wavesurfer.on('ready', function() {
          me.wavesurfer.enableDragSelection({
              color: me.randomColor(0.1)
          });

          if (me.annotations[me.pageNumber]) {
               me.loadRegions(me.annotations[me.pageNumber]); 
          }
          // else {
          //   me.loadRegions(
          //       me.extractRegions(
          //           me.wavesurfer.backend.getPeaks(512),
          //           me.wavesurfer.getDuration()
          //       )
          //   );

          // }



        });

        this.wavesurfer.on('region-click', function(region, e) {
          e.stopPropagation();
          // Play on click, loop on shift click
          e.shiftKey ? region.playLoop() : region.play();
        });
        this.wavesurfer.on('region-click', this.editAnnotation);

        this.wavesurfer.on('region-updated', this.saveRegions);
        this.wavesurfer.on('region-removed', this.saveRegions);

        //this.wavesurfer.on('region-in', this.showNote);

        this.wavesurfer.on('region-play', function(region) {
          region.once('out', function() {
              me.wavesurfer.play(region.start);
              me.wavesurfer.pause();
          });
        });
    },
    // showNote(region) {
    //     if (!showNote.el) {
    //         showNote.el = document.querySelector('#subtitle');
    //     }
    //     showNote.el.textContent = region.data.note || '–';
    // },

    editAnnotation(region) {
      var form = document.forms.edit;
      form.style.opacity = 1;
      (form.elements.start.value = Math.round(region.start * 10) / 10),
          (form.elements.end.value = Math.round(region.end * 10) / 10);
      form.elements.note.value = region.data.note || '';
      form.onsubmit = function(e) {
          e.preventDefault();
          region.update({
              start: form.elements.start.value,
              end: form.elements.end.value,
              data: {
                  note: form.elements.note.value
              }
          });
          form.style.opacity = 0;
      };
      form.onreset = function() {
          form.style.opacity = 0;
          form.dataset.region = null;
      };
      form.dataset.region = region.id;
    },

    deleteRegion(){
      var form = document.forms.edit;
      var regionId = form.dataset.region;
      if (regionId) {
          this.wavesurfer.regions.list[regionId].remove();
          form.reset();
      }
    },
    saveRegions() {
      var me = this;
      this.localStorage.regions = JSON.stringify(
          Object.keys(me.wavesurfer.regions.list).map(function(id) {
              var region = me.wavesurfer.regions.list[id];
              return {
                  start: region.start,
                  end: region.end,
                  attributes: region.attributes,
                  data: region.data
              };
          })
      );
    },

    async saveAnnotations(){
      const docId = this.docs[this.pageNumber].id;
      const payload = {
          text: this.localStorage.regions,
        };
      await HTTP.post(`docs/${docId}/annotations`, payload).then((response) => {
        this.annotations[this.pageNumber] = response.data;
      });

    },


    randomColor(alpha) {
      return (
          'rgba(' +
          [
              ~~(Math.random() * 255),
              ~~(Math.random() * 255),
              ~~(Math.random() * 255),
              alpha || 1
          ] +
          ')'
      );
    },

    loadRegions(regionstext) {
      var me = this;

      var regions = JSON.parse(regionstext[regionstext.length-1].text);

      this.localStorage.regions = regions;

      regions.forEach(function(region) {
        region.color = me.randomColor(0.1);
        me.wavesurfer.addRegion(region);
    });

    },
    togglePlayPause(){
      this.wavesurfer.playPause();
      /* Toggle play/pause buttons. */
      var playButton = document.querySelector('#play');
      var pauseButton = document.querySelector('#pause');
      this.wavesurfer.on('play', function() {
          playButton.style.display = 'none';
          pauseButton.style.display = '';
      });
      this.wavesurfer.on('pause', function() {
          playButton.style.display = '';
          pauseButton.style.display = 'none';
      });
    },

    // async submit() {
    //   const state = this.getState();
    //   this.url = `docs?q=${this.searchQuery}&speech2text_annotations__isnull=${state}&offset=${this.offset}`;
    //   await this.search();
    //   this.pageNumber = 0;
    // },


  },
});

