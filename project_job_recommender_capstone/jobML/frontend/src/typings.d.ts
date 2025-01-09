declare module "*.css" {
  interface IClassNames {
    [className: string]: string;
  }
  const classNames: IClassNames;
  export = classNames;
}
declare module 'progressbar.js' {
  export class Line {
    constructor(container: HTMLElement, options?: any);
    animate(progress: number, options?: any, callback?: () => void): void;
    setText(text: string): void;
    value(): number;
    destroy(): void;
  }
  export interface Shape {
    setText(text: string): void;
    value(): number;
    // Add any additional methods you use from the 'bar' object here.
  }

}