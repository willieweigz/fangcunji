import { Fragment } from "react";

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
                sub
              )
            )}
          </Fragment>
        )
      )}
    </>
  );
}
