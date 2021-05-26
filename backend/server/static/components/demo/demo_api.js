import MockAdatper from 'axios-mock-adapter';
import HTTP, { defaultHttpClient } from '../http';

function newId() {
  return Number((Math.random() * 100000).toFixed(0));
}

function parseOffset(url) {
  const offset = url.match(/offset=(\d+)/);
  return offset ? Number(offset[1]) : 0;
}

function parseDocId(url) {
  return Number(url.split('/')[5]);
}

function parseAnnotationId(url) {
  return Number(url.split('/')[7]);
}

export default class DemoApi {
  constructor(data, labelField) {
    this.data = data;
    this.labelField = labelField;
    this.mocks = [new MockAdatper(HTTP), new MockAdatper(defaultHttpClient)];
    this.pageSize = 5;
  }

  getMe() {
    return [200, this.data.me];
  }

  getLabels() {
    return [200, this.data.labels];
  }

  getStatistics() {
    return [200, {
      total: this.data.docs.length,
      remaining: this.data.docs.filter(doc => doc.annotations.length === 0).length,
    }];
  }

  getDocs(config) {
    const offset = parseOffset(config.url);

    return [200, {
      results: this.data.docs.slice(Math.max(offset - 1, 0), this.pageSize),
      count: this.data.docs.length,
      next: offset + this.pageSize <= this.data.docs.length
        ? config.url.replace(`offset=${offset}`, `offset=${offset + this.pageSize}`)
        : null,
      previous: offset - this.pageSize >= 0
        ? config.url.replace(`offset=${offset}`, `offset=${offset - this.pageSize}`)
        : null,
    }];
  }

  getProject() {
    return [200, this.data.project];
  }

  postAnnotations(config) {
    const docId = parseDocId(config.url);
    const body = JSON.parse(config.data);

    const doc = this.data.docs.find(_ => _.id === docId);
    if (!doc) {
      return [404, {}];
    }

    let annotation = doc.annotations.find(_ => _[this.labelField] === body[this.labelField]);
    if (!annotation) {
      annotation = { id: newId(), ...body };
      doc.annotations.push(annotation);
    }

    return [200, annotation];
  }

  deleteAnnotations(config) {
    const docId = parseDocId(config.url);
    const annotationId = parseAnnotationId(config.url);

    const doc = this.data.docs.find(_ => _.id === docId);
    if (!doc) {
      return [404, {}];
    }

    doc.annotations = doc.annotations.filter(el => el.id !== annotationId);
    return [200, {}];
  }

  start() {
    this.mocks.forEach((mock) => {
      mock.onGet(/\/v1\/.*/g).reply((config) => {
        if (config.url.endsWith('/me')) {
          return this.getMe();
        }

        if (config.url.endsWith('/labels')) {
          return this.getLabels();
        }

        if (config.url.endsWith('/statistics')) {
          return this.getStatistics();
        }

        if (config.url.indexOf('/docs') !== -1) {
          return this.getDocs(config);
        }

        return this.getProject();
      });

      mock.onPost(/\/v1\/.*/g).reply((config) => {
        if (config.url.endsWith('/annotations')) {
          return this.postAnnotations(config);
        }

        return [404, {}];
      });

      mock.onDelete(/\/v1\/.*/g).reply((config) => {
        if (config.url.indexOf('/annotations') !== -1) {
          return this.deleteAnnotations(config);
        }

        return [404, {}];
      });
    });
  }

  stop() {
    this.mocks.forEach(mock => mock.reset());
  }
}
