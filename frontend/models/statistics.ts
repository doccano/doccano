export type Label = {[key: string]: number}

export type User = {[key: string]: number}

export class Statistics {
  constructor(
    public label:      Label,
    public userLabel:  User,
    public total:      number,
    public remaining:  number,
    public user:       User
  ) {}

  static valueOf(
    { label, user_label, total, remaining, user }:
    {
      label:      Label,
      user_label: User,
      total:      number,
      remaining:  number,
      user:       User
    }
  ): Statistics {
    return new Statistics(label, user_label, total, remaining, user)
  }

  private makeData(object: Label | User, label: string) {
    const labels = object ? Object.keys(object) : []
    const counts = object ? Object.values(object) : []
    return {
      labels,
      datasets: [{
        label,
        backgroundColor: '#00d1b2',
        data: counts
      }]
    }
  }

  public labelStats(label: string) {
    return this.makeData(this.label, label)
  }

  public userStats(label: string) {
    return this.makeData(this.user, label)
  }

  public progress(labels: string[]) {
    const complete = this.total - this.remaining
    const incomplete = this.remaining
    return {
      datasets: [{
        data: [complete, incomplete],
        backgroundColor: ['#00d1b2', '#ffdd57']
      }],
      labels
    }
  }
}
