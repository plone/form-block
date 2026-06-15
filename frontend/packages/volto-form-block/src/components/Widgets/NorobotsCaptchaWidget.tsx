import TextWidget from '@plone/volto/components/manage/Widgets/TextWidget';

type NoRobotsCaptchaWidgetProps = {
  id: string;
  title?: string;
  value: string;
  onEdit?: boolean;
  onChange: (id: string, value: string) => void;
  captcha_props: { id: string; title?: string };
};

const NoRobotsCaptchaWidget = ({
  id,
  title,
  value,
  onEdit,
  onChange,
  captcha_props,
}: NoRobotsCaptchaWidgetProps) => {
  const titleValue = captcha_props?.title || title;

  return onEdit ? (
    <></>
  ) : (
    <TextWidget
      id={id}
      name={captcha_props.id}
      label={titleValue}
      title={titleValue}
      onChange={onChange}
      required={true}
      value={value}
    />
  );
};

export default NoRobotsCaptchaWidget;
