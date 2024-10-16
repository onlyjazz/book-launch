// CustomMarkdownInput.tsx
import {MarkdownInput, MarkdownInputProps} from 'sanity-plugin-markdown'
import {JSX, useMemo} from "react";

export function CustomMarkdownInput(props: JSX.IntrinsicAttributes & MarkdownInputProps) {
  const reactMdeProps: MarkdownInputProps['reactMdeProps'] = useMemo(() => {
    return {
      "options": {
        "toolbar": ['bold', 'italic'],
        // more options available, see:
        // https://github.com/Ionaru/easy-markdown-editor#options-list
      },
      // more props available, see:
      // https://github.com/RIP21/react-simplemde-editor#react-simplemde-easymde-markdown-editor
    }
  }, [])

  return <MarkdownInput {...props} reactMdeProps={reactMdeProps} />
}
