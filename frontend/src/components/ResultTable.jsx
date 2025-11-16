import { useMemo } from "react";
import { useTable, useSortBy } from "react-table";

export default function ResultTable({ rows }) {
  const data = useMemo(() => rows, [rows]);
  const columns = useMemo(() => {
    if (!rows || rows.length === 0) return [];
    return Object.keys(rows[0]).map((key) => ({
      Header: key,
      accessor: key
    }));
  }, [rows]);

  const tableInstance = useTable({ columns, data }, useSortBy);
  const { getTableProps, getTableBodyProps, headerGroups, rows: tableRows, prepareRow } =
    tableInstance;

  if (!rows || rows.length === 0) return null;

  return (
    <section className="card">
      <h2>Résultats V2</h2>
      <div className="table-wrapper">
        <table {...getTableProps()}>
          <thead>
            {headerGroups.map((headerGroup) => {
              const headerGroupProps = headerGroup.getHeaderGroupProps();
              const { key: headerGroupKey, ...headerGroupRest } = headerGroupProps;
              return (
                <tr {...headerGroupRest} key={headerGroupKey || headerGroup.id}>
                  {headerGroup.headers.map((column) => {
                    const headerProps = column.getHeaderProps(column.getSortByToggleProps());
                    const { key: headerKey, ...headerRest } = headerProps;
                    return (
                      <th key={headerKey || column.id} {...headerRest}>
                        {column.render("Header")}
                        <span>
                          {column.isSorted ? (column.isSortedDesc ? " 🔽" : " 🔼") : ""}
                        </span>
                      </th>
                    );
                  })}
                </tr>
              );
            })}
          </thead>
          <tbody {...getTableBodyProps()}>
            {tableRows.map((row) => {
              prepareRow(row);
              const rowProps = row.getRowProps();
              const { key: rowKey, ...rowRest } = rowProps;
              return (
                <tr {...rowRest} key={rowKey || row.id}>
                  {row.cells.map((cell) => {
                    const cellProps = cell.getCellProps();
                    const { key: cellKey, ...cellRest } = cellProps;
                    return (
                      <td key={cellKey || cell.column.id} {...cellRest}>
                        {cell.render("Cell")}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
