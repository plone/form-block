import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getFormData } from '@plone/volto-form-block/actions/form';
import {
  selectBlockItems,
  type FormDataState,
  type StoredFormItem,
} from '@plone/volto-form-block/helpers/datatable';

/**
 * Load and track the stored submissions for a form block.
 *
 * Fetches on mount and again whenever the stored data is cleared, then filters
 * the result down to the submissions belonging to ``blockId``.
 *
 * :param path: The app-relative path of the form's content object.
 * :param blockId: The id of the form block whose submissions to load.
 * :returns: The submissions belonging to the block.
 */
export function useStoredFormData(
  path: string,
  blockId: string,
): StoredFormItem[] {
  const dispatch = useDispatch();
  const formData = useSelector(
    (state: { formData: FormDataState }) => state.formData,
  );
  const clearFormDataSelector = useSelector(
    (state: { clearFormData: { loaded: boolean } }) => state.clearFormData,
  );
  const [data, setData] = useState<StoredFormItem[]>([]);

  useEffect(() => {
    dispatch(getFormData(path, blockId));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clearFormDataSelector.loaded]);

  useEffect(() => {
    setData(selectBlockItems(formData, blockId));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [formData]);

  return data;
}
