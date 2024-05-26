import { TextField } from "mdui";

type SettingsType = {
  fps: number;
  ups: number;
};

// export const Settings = {
//   settings: new Proxy<SettingsType>(
//     // 默认设置
//     { fps: 1, ups: 3 },
//     {
//       get(target, key: keyof SettingsType) {
//         const lc = JSON.parse(
//           localStorage.getItem("settings") || "{}"
//         ) as SettingsType;
//         return lc[key] ?? target[key];
//       },
//       set(_target, key: keyof SettingsType, value: any) {
//         const lc = JSON.parse(
//           localStorage.getItem("settings") || "{}"
//         ) as SettingsType;
//         lc[key] = value;
//         localStorage.setItem("settings", JSON.stringify(lc));
//         return true;
//       },
//     }
//   ),
//   init(): void {
//     const settingsDialog = document.getElementById("settings-dialog");
//     for (const el of settingsDialog?.children!) {
//       const field = el.querySelector<TextField>("[data-key]")!;
//       const key = field.dataset.key!;
//       // @ts-expect-error
//       field.value = this.settings[key];
//       field.addEventListener("change", () => {
//         const value = field.value;
//         // @ts-expect-error
//         this.settings[key] = value;
//         console.log(key, value);
//       });
//     }
//   },
// };

export const Settings = new Proxy<SettingsType & { init(): void }>(
  // 默认设置
  {
    fps: 1,
    ups: 3,
    init(): void {
      const settingsDialog = document.getElementById("settings-dialog");
      for (const el of settingsDialog?.children!) {
        const field = el.querySelector<TextField>("[data-key]")!;
        const key = field.dataset.key!;
        // @ts-expect-error
        field.value = this[key];
        field.addEventListener("change", () => {
          const value = field.value;
          // @ts-expect-error
          this[key] = value;
          console.log(key, value);
        });
      }
    },
  },
  {
    get(target, key: keyof SettingsType | "init") {
      if (key === "init") {
        return target[key];
      }
      const lc = JSON.parse(
        localStorage.getItem("settings") || "{}"
      ) as SettingsType;
      return lc[key] ?? target[key];
    },
    set(_target, key: keyof SettingsType | "init", value: any) {
      if (key === "init") {
        return true;
      }
      const lc = JSON.parse(
        localStorage.getItem("settings") || "{}"
      ) as SettingsType;
      lc[key] = value;
      localStorage.setItem("settings", JSON.stringify(lc));
      return true;
    },
  }
);
