import React from 'react'
import FlatButton from 'material-ui/FlatButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import Dialog from 'material-ui/Dialog'

class UserReportCard extends React.Component {

  constructor() {
    super()
    this.state = {
      modalOpen: false,
      modalInfo: {}
    }
    this.modalActions = [
      <FlatButton
        label="Cancel"
        primary={true}
        onTouchTap={this._handleCloseModal.bind(this)}
      />
    ]
  }

  render() {
    return(
      <div>
        <Table selectable={false}>
          <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
            <TableRow>
              <TableHeaderColumn>Happiness</TableHeaderColumn>
              <TableHeaderColumn>Date</TableHeaderColumn>
              <TableHeaderColumn>Actions</TableHeaderColumn>
            </TableRow>
          </TableHeader>
          <TableBody displayRowCheckbox={false}>
            {this.props.reports.map((report, key) => (
              <TableRow key={key}>
                <TableRowColumn>{report.happiness}</TableRowColumn>
                <TableRowColumn>{this._getDate(report.date)}</TableRowColumn>
                <TableRowColumn>
                  {report.comments ? <FlatButton label="See comments" onClick={this._showCommentsModal.bind(this, report)} /> : ''}
                </TableRowColumn>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <Dialog
          title="Report comments"
          modal={false}
          actions={this.modalActions}
          open={this.state.modalOpen}>
          {this.state.modalInfo.comments ? this.state.modalInfo.comments : ''}
        </Dialog>

      </div>
    )
  }

  _getDate(date) {
    return `${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`
  }

  _showCommentsModal(report) {
    this.setState({ modalOpen: true, modalInfo: report })
  }

  _handleCloseModal() {
    this.setState({ modalOpen: false, modalInfo: {} })
  }

}

export default UserReportCard
