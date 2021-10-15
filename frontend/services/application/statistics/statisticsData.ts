import { Statistics } from '~/domain/models/statistics/statistics'


export class StatisticsDTO {
  label: object;
  user: object;
  progress: object;
  annotatorProgress: object;
  approverProgress: object;
  adminProgress: object;

  constructor(item: Statistics, labelText: string, userText: string, progressLabels: string[]) {
    this.label = item.labelStats(labelText);
    this.user = item.userStats(userText);
    this.progress = item.progress(progressLabels);
    this.annotatorProgress = item.annotatorProgress(progressLabels);
    this.approverProgress = item.approverProgress(progressLabels);
    this.adminProgress = item.adminProgress(progressLabels);
  }
}
