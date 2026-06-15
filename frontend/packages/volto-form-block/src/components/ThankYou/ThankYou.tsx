import React from 'react';
import { Message } from 'semantic-ui-react';

interface ThankYouProps {
  data: Record<string, any>;
  formfields: string;
  submittedData: Record<string, any>;
}
const ThankYou: React.FC<ThankYouProps> = (props) => {
  const { data, formfields, submittedData } = props;

  let thankyou = data.thankyou || '';

  // Add formfields
  thankyou = thankyou.replace('${formfields}', formfields); // eslint-disable-line no-template-curly-in-string

  // Add seperate fields
  Object.keys(submittedData).forEach((field) => {
    thankyou = thankyou.replace('${' + field + '}', submittedData[field]);
  });

  return (
    <div className="submitted">
      <Message positive>
        <p>{data.success}</p>
      </Message>
      <p
        className="thankyou"
        dangerouslySetInnerHTML={{
          __html: thankyou,
        }}
      />
    </div>
  );
};

export default ThankYou;
