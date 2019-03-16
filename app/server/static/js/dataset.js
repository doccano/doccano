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
    if (docsCount && Number.parseInt(docsCount, 10)) {
        bulmaToast.toast({
            message: `Successfully imported ${docsCount} records.`,
            type: 'is-success',
            position: 'top-center',
        });
    }
    window.history.replaceState(null, null, window.location.pathname);
  }
});
