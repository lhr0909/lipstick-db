export interface Lipstick {
  id: string;
  brand: string;
  color: string;
  nickname: string;
  meta: { [key: string]: any };
  product_image: string;
  trial_images: Array<{
    id: string;
    uri: string;
  }>;
}

export interface LipstickTrialImageColors {
  id: string;
  parent_id: string;
  modality: string;
  tensor: number[][];
  embedding: number[];
  scores?: any;
}

export const LIPSTICK_TAG_COLORS: { [key: string]: string } = {
  '口红': 'magenta',
  '唇釉': 'cyan',
  '哑光': 'blue',
  '亮面': 'green',
};

export interface S3UploadResponse {
  url: string;
  filename: string;
  fields: { [key: string]: string };
}

export interface SearchMatch {
  lipstick_id: string;
  trial_image_id: string;
  score: number;
}

export interface SearchResult {
  matches: SearchMatch[];
}
