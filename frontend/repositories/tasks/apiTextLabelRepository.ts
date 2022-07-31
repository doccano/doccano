import { AnnotationRepository } from '@/domain/models/tasks/annotationRepository'
import { TextLabel } from '@/domain/models/tasks/textLabel'

export class APITextLabelRepository extends AnnotationRepository<TextLabel> {
  labelName = 'texts'

  toModel(item: { [key: string]: any }): TextLabel {
    return new TextLabel(item.id, item.text, item.user)
  }

  toPayload(item: TextLabel): { [key: string]: any } {
    return {
      id: item.id,
      text: item.text,
      user: item.user
    }
  }
}
