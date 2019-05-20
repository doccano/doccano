import Vue from 'vue';
import * as bulmaToast from 'bulma-toast';

const removeUrlParam = (name) => {
	const [ head, tail ] = location.href.split( '?' );
	location.href = head + '?' + tail.replace( new RegExp( `&${name}=[^&]*|${name}=[^&]*&` ), '' );
}

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mounted () {
    const urlParams = new URLSearchParams(window.location.search);
    const docsCount = urlParams.get('docs_count');
    const labelsCount = urlParams.get('true_labels_count')
    const usersLabelsCount = urlParams.get('true_labels_count')
    if (docsCount && Number.parseInt(docsCount, 10)) {
        bulmaToast.toast({
            message: `Successfully imported ${docsCount} records.`,
            type: 'is-success',
            position: 'top-center',
        });
    }

    if (labelsCount && Number.parseInt(labelsCount, 10)) {
      bulmaToast.toast({
          message: `Successfully imported ${labelsCount} true labels.`,
          type: 'is-success',
          position: 'top-center',
      });
    }
    
    if (usersLabelsCount && Number.parseInt(usersLabelsCount, 10)) {
      bulmaToast.toast({
          message: `Successfully imported ${usersLabelsCount} users labels.`,
          type: 'is-success',
          position: 'top-center',
      });
    } 

    window.history.replaceState(null, null, window.location.pathname);
  }
});
