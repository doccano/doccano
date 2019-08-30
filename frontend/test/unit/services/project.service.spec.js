import MockAdapter from 'axios-mock-adapter'
import ProjectService from '@/services/project.service.js'

describe('Project.service', () => {
  const mockAxios = new MockAdapter(ProjectService.request.instance)

  test('can get project list', async () => {
    const data = [
      {
        id: 1,
        name: 'CoNLL 2003',
        description: 'This is a project for NER.',
        guideline: 'Please write annotation guideline.',
        users: [1],
        project_type: 'SequenceLabeling',
        image: '/static/assets/images/cats/sequence_labeling.jpg',
        updated_at: '2019-07-09T06:19:29.789091Z',
        randomize_document_order: false,
        resourcetype: 'SequenceLabelingProject'
      }
    ]
    mockAxios.onGet('/projects').reply(200, data)
    const response = await ProjectService.getProjectList()
    expect(response).toEqual(data)
  })

  test('can create a project', async () => {
    const data = {
      name: 'test project',
      description: 'test description',
      guideline: 'Please write annotation guideline.',
      project_type: 'SequenceLabeling',
      randomize_document_order: false
    }
    mockAxios.onPost('/projects').reply(201, data)
    const response = await ProjectService.createProject(data)
    expect(response.title).toEqual(data.title)
  })

  test('can delete a project', async () => {
    const projectId = 1
    mockAxios.onDelete(`/projects/${projectId}`).reply(204, {})
    const response = await ProjectService.deleteProject(projectId)
    expect(response).toEqual({})
  })
})
