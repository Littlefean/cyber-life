import { invoke } from "@tauri-apps/api";

export const Life = {
  init() {},

  async render(ctx: CanvasRenderingContext2D) {
    // update
    const cpuCount = await invoke<number>("cpu_count");
    const memory = await invoke<number>("memory");
    const cpu = await invoke<number>("cpu");

    // draw
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = "red";
    ctx.fillRect(0, 0, memory * ctx.canvas.width, 10);
    ctx.fillRect(0, 10, cpu * ctx.canvas.width, 10);
  },
};
