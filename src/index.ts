#!/usr/bin/env node
import chalk from "chalk";

interface Field {
  key: string;
  value: string;
}

interface Section {
  title: string;
  fields: Field[];
}

const WIDTH = 62;

/** Renders "Key: ....... Value" with dot-leader padding, neofetch-style. */
function field(key: string, value: string): string {
  const label = chalk.magenta(key);
  const val = value
    .replace(/[\d,]+\+\+/g, (match) => chalk.green(match))
    .replace(/[\d,]+--/g, (match) => chalk.red(match));
  const rawLen = key.length + value.length + 2;
  const dotsCount = Math.max(2, WIDTH - rawLen);
  const dots = chalk.gray(".".repeat(dotsCount));
  return `  ${label}: ${dots} ${val}`;
}

/** Renders a section divider line, e.g. "- Contact --------------" */
function header(title: string): string {
  const bar = "-".repeat(Math.max(0, WIDTH - title.length - 1));
  return `\n${chalk.bold(title)} ${chalk.gray(bar)}`;
}

// ---- Edit everything below to make this yours ----

const sections: Section[] = [
  {
    title: "abdulkareem@dev",
    fields: [
      { key: "OS", value: "Arch Linux" },
      { key: "Uptime", value: "20 years" },
      // { key: "Host", value: "COMSATS University Islamabad, Lahore Campus" },
      // { key: "Kernel", value: "CAM (Computer Aided Manufacturing) Operator" },
      { key: "IDE", value: "Neovim" },
      { key: "Languages.Programming", value: "Python, TypeScript, Go, C++" },
      { key: "Languages.Computer", value: "HTML, CSS, JSON, Typst, YAML" },
      { key: "Languages.Real", value: "English" },
      { key: "Hobbies.Software", value: "Minecraft Modding" },
      { key: "Hobbies.Hardware", value: "Homelab, Chess" },
    ],
  },
  {
    title: "- Contact",
    fields: [
      { key: "Website", value: "abdulkareem.me" },
      { key: "Email", value: "ak@abdulkareem.me" },
      // { key: "Email.Personal", value: "andrew@grant.software" },
      // { key: "Email.Work", value: "Andrew.Grant@ttmtech.com" },
      { key: "GitHub", value: "abdulkareemakn"},
      { key: "LinkedIn", value: "abdul-kareem-nasir" },
      { key: "Discord", value: "tmtaxman" },
    ],
  },
  {
    title: "- GitHub Stats",
    fields: [
      { key: "Repos", value: "25 {Contributed: 49}" },
      { key: "Stars", value: "1" },
      { key: "Commits", value: "1,390" },
      { key: "Followers", value: "2" },
      { key: "Lines of Code on GitHub", value: "1,281,593 (1,425,703++, 144,110--)" },
    ],
  },
];

function render(): void {
  for (const section of sections) {
    console.log(header(section.title));
    for (const f of section.fields) {
      if (f.key === "Languages.Programming" || f.key === "Hobbies.Software") console.log("");
      console.log(field(f.key, f.value));
    }
  }
  console.log("");
}

render();
