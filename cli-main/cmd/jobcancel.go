package cmd

import (
	"context"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/spf13/cobra"

	"github.com/render-oss/cli/pkg/command"
	"github.com/render-oss/cli/pkg/text"
	"github.com/render-oss/cli/pkg/tui/views"
)

var jobCancelCmd = &cobra.Command{
	Use:   "cancel <serviceID> <jobID>",
	Short: "Cancel a running job",
	Args:  cobra.ExactArgs(2),
}

var InteractiveJobCancel = func(ctx context.Context, input views.JobCancelInput, breadcrumb string) tea.Cmd {
	return command.AddToStackFunc(ctx, jobCancelCmd, breadcrumb, &input, views.NewJobCancelView(ctx, input))
}

func init() {
	jobCancelCmd.RunE = func(cmd *cobra.Command, args []string) error {
		var input views.JobCancelInput
		err := command.ParseCommand(cmd, args, &input)
		if err != nil {
			return err
		}

		if nonInteractive, err := command.NonInteractiveWithConfirm(
			cmd,
			cancelJob(cmd, input),
			text.FormatString,
			confirmJobCancel(cmd, input),
		); err != nil {
			return err
		} else if nonInteractive {
			return nil
		}

		InteractiveJobCancel(cmd.Context(), input, "Cancel job "+input.JobID)
		return nil
	}
}

func cancelJob(cmd *cobra.Command, input views.JobCancelInput) func() (string, error) {
	return func() (string, error) {
		return views.CancelJob(cmd.Context(), input)
	}
}

func confirmJobCancel(cmd *cobra.Command, input views.JobCancelInput) func() (string, error) {
	return func() (string, error) {
		return views.RequireConfirmationForCancelJob(cmd.Context(), input)
	}
}
