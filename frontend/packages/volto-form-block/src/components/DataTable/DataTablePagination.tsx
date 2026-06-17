import type { FC } from 'react';
import Icon from '@plone/volto/components/theme/Icon/Icon';
import paginationLeftSVG from '@plone/volto/icons/left-key.svg';
import paginationRightSVG from '@plone/volto/icons/right-key.svg';
import { Pagination, type PaginationProps } from 'semantic-ui-react';
import type { Table as ReactTableInstance } from '@tanstack/react-table';
import type { StoredFormItem } from '@plone/volto-form-block/helpers/datatable';

interface DataTablePaginationProps {
  /** The react-table instance driving the pagination. */
  table: ReactTableInstance<StoredFormItem>;
}

/**
 * Page navigation for the DataTable; renders nothing for a single page.
 */
const DataTablePagination: FC<DataTablePaginationProps> = ({ table }) => {
  if (table.getPageCount() <= 1) {
    return null;
  }
  const page = table.getState().pagination.pageIndex + 1;
  const pageCount = table.getPageCount();

  return (
    <div className="pagination-wrapper react-table-pagination">
      <Pagination
        activePage={page}
        totalPages={pageCount}
        onPageChange={(_event, { activePage }: PaginationProps) => {
          table.setPageIndex(Number(activePage) - 1);
        }}
        firstItem={null}
        lastItem={null}
        prevItem={{
          content: <Icon name={paginationLeftSVG} size="18px" />,
          icon: true,
          'aria-disabled': page === 1,
          className: page === 1 ? 'disabled' : null,
        }}
        nextItem={{
          content: <Icon name={paginationRightSVG} size="18px" />,
          icon: true,
          'aria-disabled': page === pageCount,
          className: page === pageCount ? 'disabled' : null,
        }}
      ></Pagination>
    </div>
  );
};

export default DataTablePagination;
