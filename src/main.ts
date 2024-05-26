import {
  LogicalPosition,
  LogicalSize,
  appWindow,
  primaryMonitor,
} from "@tauri-apps/api/window";
import { Settings } from "./settings";

import "mdui/mdui.css";
import "mdui";

import "./styles.css";
import type { Button, Dialog } from "mdui";
import { LifeManager } from "./life/LifeManager";

const setToTop = () => {
  appWindow.show();
  appWindow.setAlwaysOnTop(false);
  requestAnimationFrame(() => {
    appWindow.setAlwaysOnTop(true);
  });
};

let lastRender = 0;
let lastUpdate = 0;
const tick: FrameRequestCallback = (time) => {
  requestAnimationFrame(tick);
  // 计算时间间隔
  let renderDelta = time - lastRender;
  // 如果时间间隔大于或等于目标帧间隔，则渲染下一帧
  if (renderDelta >= 1000 / Settings.fps) {
    lastRender = time - (renderDelta % (1000 / Settings.fps));
    // 在这里执行渲染逻辑
    LifeManager.render(
      (document.getElementById("canvas") as HTMLCanvasElement).getContext("2d")!
    );
  }
  let updateDelta = time - lastUpdate;
  if (updateDelta >= 1000 / Settings.ups) {
    lastUpdate = time - (renderDelta % (1000 / Settings.ups));
    LifeManager.update();
  }
};

(async () => {
  // dom
  const settingsBtn = document.getElementById("settings-btn") as Button;
  const settingsDialog = document.getElementById("settings-dialog") as Dialog;
  const aboutBtn = document.getElementById("about-btn") as Button;
  const aboutDialog = document.getElementById("about-dialog") as Dialog;
  const canvas = document.getElementById("canvas") as HTMLCanvasElement;

  const mon = await primaryMonitor();
  const x = (mon?.size.width ?? 1920) - 50 - 250;
  const y = (mon?.size.height ?? 1920) - 50 - 48 - 130; // 任务栏48px
  const w = 250;
  const h = 130;
  // 打开弹窗页面时窗口大小偏移量
  const dw = 50;
  const dy = 300;
  appWindow.setSize(new LogicalSize(w, h));
  appWindow.setPosition(new LogicalPosition(x, y));

  settingsBtn.addEventListener("click", () => {
    appWindow.setSize(new LogicalSize(w + dw, h + dy));
    appWindow.setPosition(new LogicalPosition(x - dw, y - dy));
    settingsDialog.open = true;
  });
  settingsDialog.addEventListener("closed", () => {
    appWindow.setSize(new LogicalSize(w, h));
    appWindow.setPosition(new LogicalPosition(x, y));
  });

  aboutBtn.addEventListener("click", () => {
    appWindow.setSize(new LogicalSize(w + dw, h + dy));
    appWindow.setPosition(new LogicalPosition(x - dw, y - dy));
    aboutDialog.open = true;
  });
  aboutDialog.addEventListener("closed", () => {
    appWindow.setSize(new LogicalSize(w, h));
    appWindow.setPosition(new LogicalPosition(x, y));
  });

  Settings.init();
  setInterval(setToTop, 500);
  canvas.width = w;
  canvas.height = h;

  requestAnimationFrame(tick);
})();