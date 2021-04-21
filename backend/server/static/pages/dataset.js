import HTTP from '../components/http';

document.querySelectorAll('.delete-document-button').forEach((deleteButton) => {
  deleteButton.addEventListener('click', () => {
    const documentId = deleteButton.getAttribute('data-delete-document-id');
    HTTP.delete(`docs/${documentId}`).then(() => window.location.reload());
  });
});
