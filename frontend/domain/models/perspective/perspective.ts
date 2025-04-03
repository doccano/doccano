export interface PerspectiveItem {
    id?: number;
    userId: number;
    projectId: number;
    subject: string;
    text: string;
    category: 'cultural' | 'technic' | 'subjective';
    createdAt?: string;
    updatedAt?: string;
}