import Vue from 'vue';
import annotationMixin from './mixin';
import HTTP from './http';

Vue.use(require('vue-shortkey'));

 

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
     wavesurfer: null,
  },
  mixins: [annotationMixin],
  directives: {},

  updated () {
    this.$nextTick(() => {
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

          if (me.localStorage.regions) {
              me.loadRegions(JSON.parse(me.localStorage.regions));
          }else {
            me.loadRegions(
                me.extractRegions(
                    me.wavesurfer.backend.getPeaks(512),
                    me.wavesurfer.getDuration()
                )
            );

          }



        });

        this.wavesurfer.on('region-click', function(region, e) {
          e.stopPropagation();
          // Play on click, loop on shift click
          e.shiftKey ? region.playLoop() : region.play();
        });
        this.wavesurfer.on('region-click', this.editAnnotation);

        this.wavesurfer.on('region-updated', this.saveRegions);
        this.wavesurfer.on('region-removed', this.saveRegions);

        this.wavesurfer.on('region-in', this.showNote);

        this.wavesurfer.on('region-play', function(region) {
          region.once('out', function() {
              me.wavesurfer.play(region.start);
              me.wavesurfer.pause();
          });
        });
    },
    showNote(region) {
        if (!showNote.el) {
            showNote.el = document.querySelector('#subtitle');
        }
        showNote.el.textContent = region.data.note || '–';
    },

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

    loadRegions(regions) {
      var me = this;
      this.regions.forEach(function(region) {
        region.color = me.randomColor(0.1);
        me.wavesurfer.addRegion(region);
    });
    },
    togglePlayPause(){
      this.wavesurfer.playPause();
    },

    extractRegions(peaks, duration) {
      // Silence params
      var minValue = 0.0015;
      var minSeconds = 0.25;

      var length = peaks.length;
      var coef = duration / length;
      var minLen = minSeconds / coef;

      // Gather silence indeces
      var silences = [];
      Array.prototype.forEach.call(peaks, function(val, index) {
          if (Math.abs(val) <= minValue) {
              silences.push(index);
          }
      });

      // Cluster silence values
      var clusters = [];
      silences.forEach(function(val, index) {
          if (clusters.length && val == silences[index - 1] + 1) {
              clusters[clusters.length - 1].push(val);
          } else {
              clusters.push([val]);
          }
      });

      // Filter silence clusters by minimum length
      var fClusters = clusters.filter(function(cluster) {
          return cluster.length >= minLen;
      });

      // Create regions on the edges of silences
      var regions = fClusters.map(function(cluster, index) {
          var next = fClusters[index + 1];
          return {
              start: cluster[cluster.length - 1],
              end: next ? next[0] : length - 1
          };
      });

      // Add an initial region if the audio doesn't start with silence
      var firstCluster = fClusters[0];
      if (firstCluster && firstCluster[0] != 0) {
          regions.unshift({
              start: 0,
              end: firstCluster[firstCluster.length - 1]
          });
      }

      // Filter regions by minimum length
      var fRegions = regions.filter(function(reg) {
          return reg.end - reg.start >= minLen;
      });

      // Return time-based regions
      return fRegions.map(function(reg) {
          return {
              start: Math.round(reg.start * coef * 10) / 10,
              end: Math.round(reg.end * coef * 10) / 10
          };
      });
  },


  },
});

