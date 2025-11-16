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
              return (
                <tr {...headerGroupProps} key={headerGroupProps.key || headerGroup.id}>
                  {headerGroup.headers.map((column) => {
                    const headerProps = column.getHeaderProps(column.getSortByToggleProps());
                    return (
                      <th key={headerProps.key || column.id} {...headerProps}>
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
              return (
                <tr {...rowProps} key={rowProps.key || row.id}>
                  {row.cells.map((cell) => {
                    const cellProps = cell.getCellProps();
                    return (
                      <td key={cellProps.key || cell.column.id} {...cellProps}>
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
