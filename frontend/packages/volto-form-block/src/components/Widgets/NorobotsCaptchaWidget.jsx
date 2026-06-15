import TextWidget from '@plone/volto/components/manage/Widgets/TextWidget';

const NoRobotsCaptchaWidget = ({
  id,
  title,
  value,
  onEdit,
  onChange,
  captcha_props,
}) => {
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
      value={value}
    />
  );
};

export default NoRobotsCaptchaWidget;
