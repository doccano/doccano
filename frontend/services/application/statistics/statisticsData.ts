import { Statistics } from '@/models/statistics'


export class StatisticsDTO {
  label: object;
  user: object;
  progress: object;

  constructor(item: Statistics, labelText: string, userText: string, progressLabels: string[]) {
    this.label = item.labelStats(labelText);
    this.user = item.userStats(userText);
    this.progress = item.progress(progressLabels);
  }
}
