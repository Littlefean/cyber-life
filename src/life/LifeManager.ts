import { invoke } from "@tauri-apps/api";

export const LifeManager = {
  cpuCount: 0,
  memory: 0,
  cpu: 0,

  async update() {
    this.cpuCount = await invoke<number>("cpu_count");
    this.memory = await invoke<number>("memory");
    this.cpu = await invoke<number>("cpu");
  },

  render(ctx: CanvasRenderingContext2D) {
    console.log(this);
    // draw
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = "red";
    ctx.fillRect(0, 0, this.memory * ctx.canvas.width, 10);
    ctx.fillRect(0, 10, this.cpu * ctx.canvas.width, 10);
  },
};
