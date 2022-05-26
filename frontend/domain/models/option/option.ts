export class PageNumber {
  num: number

  constructor(public page: number) {
    if (typeof page === 'string' && /^\d+$/.test(page)) {
      this.num = parseInt(page, 10)
    }
    if (typeof page === 'number' && page > 0) {
      this.num = page
    }
    this.num = 1
  }
}

export class OptionItem {
  constructor(public page: number, public q?: string, public isChecked?: string) {}

  static valueOf({
    page,
    q = '',
    isChecked = ''
  }: {
    page: number
    q?: string
    isChecked?: string
  }): OptionItem {
    return new OptionItem(page, q, isChecked)
  }

  toObject(): Object {
    return {
      page: this.page,
      q: this.q,
      isChecked: this.isChecked
    }
  }
}
