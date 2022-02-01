import { Expose } from 'class-transformer'

export class LabelItem {
  id: number;
  text: string;

  @Expose({ name: 'prefix_key' })
  prefixKey: string | null;

  @Expose({ name: 'suffix_key' })
  suffixKey: string | null;

  @Expose({ name: 'background_color' })
  backgroundColor: string;

  @Expose({ name: 'text_color' })
  textColor: string = '#ffffff';

  toObject() {
    return {
      id: this.id,
      text: this.text,
      prefix_key: this.prefixKey,
      suffix_key: this.suffixKey,
      background_color: this.backgroundColor,
      text_color: this.textColor
    }
  }
}

export class DocTypeItem extends LabelItem {}
export class SpanTypeItem extends LabelItem {}
