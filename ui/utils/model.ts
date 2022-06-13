export interface Lipstick {
  id: string;
  brand: string;
  color: string;
  nickname: string;
  meta: { [key: string]: any };
  product_image: string;
}

export const LIPSTICK_TAG_COLORS: { [key: string]: string } = {
  '口红': 'magenta',
  '唇釉': 'cyan',
  '哑光': 'blue',
  '亮面': 'green',
};