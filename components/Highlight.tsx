import { Fragment } from "react";

// 自动识别"第一图/第二枚"这类分述每枚画面的序数词，加粗标记（不占用黄底强调，
// 避免和地名/人名的高亮混在一起分不清），方便快速扫出介绍的段落结构
const ORDINAL_RE = /(第[一二三四五六七八九十百]+(?:图|枚))/;

function renderPlain(text: string, keyPrefix: string) {
  // 正则带捕获组时 split 结果里奇数下标就是命中的序数词，偶数下标是周围普通文本
  return text
    .split(ORDINAL_RE)
    .map((seg, i) =>
      i % 2 === 1 ? (
        <span key={`${keyPrefix}-${i}`} className="font-bold text-postal">
          {seg}
        </span>
      ) : (
        <Fragment key={`${keyPrefix}-${i}`}>{seg}</Fragment>
      )
    );
}

// 渲染带 **标记** 的文本：标记部分（如地名）以黄底红字突出
// 自动高亮"未发行"字样：黄底红字，醒目提示
export default function Highlight({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((part, i) =>
        part.startsWith("**") && part.endsWith("**") ? (
          <span
            key={i}
            className="rounded-sm bg-yellow-300 px-1 text-seal"
          >
            {part.slice(2, -2)}
          </span>
        ) : (
          <Fragment key={i}>
            {part.split(/(未发行)/g).map((sub, j) =>
              sub === "未发行" ? (
                <span
                  key={`${i}-${j}`}
                  className="rounded-sm bg-yellow-300 px-1 text-seal"
                >
                  未发行
                </span>
              ) : (
                renderPlain(sub, `${i}-${j}`)
              )
            )}
          </Fragment>
        )
      )}
    </>
  );
}
