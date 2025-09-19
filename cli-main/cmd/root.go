/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"errors"
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/spf13/cobra"

	"github.com/render-oss/cli/pkg/cfg"
	"github.com/render-oss/cli/pkg/command"
	"github.com/render-oss/cli/pkg/config"
	renderstyle "github.com/render-oss/cli/pkg/style"
	"github.com/render-oss/cli/pkg/tui"
	"github.com/render-oss/cli/pkg/tui/views"
)

var welcomeMsg = lipgloss.NewStyle().Bold(true).Foreground(renderstyle.ColorFocus).
	Render("Render CLI v" + cfg.Version)

var longHelp = fmt.Sprintf(`%s

Welcome! Use the Render CLI to manage your services, datastores, and
environments directly from the command line. Trigger deploys, view logs,
start psql/SSH sessions, and more.

The CLI's default %s mode provides intuitive, menu-based navigation.

To use in %s mode (such as in a script), set each command's --output
option to either json or yaml for structured responses.
`, welcomeMsg, renderstyle.Bold("interactive"), renderstyle.Bold("non-interactive"))

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use: "render",

	Short: "Interact with resources on Render",
	Long:  longHelp,
	PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
		ctx := cmd.Context()

		if err := checkForDeprecatedFlagUsage(cmd); err != nil {
			return err
		}

		confirmFlag, err := cmd.Flags().GetBool(command.ConfirmFlag)
		if err != nil {
			panic(err)
		}

		ctx = command.SetConfirmInContext(ctx, confirmFlag)

		outputFlag, err := cmd.Flags().GetString("output")
		if err != nil {
			panic(err)
		}

		output, err := command.StringToOutput(outputFlag)
		if err != nil {
			println(err.Error())
			os.Exit(1)
		}
		// Honor the output flag if it's set
		if outputFlag == "" && output.Interactive() && (isPipe() || isCI()) {
			output = command.TEXT
		}
		ctx = command.SetFormatInContext(ctx, &output)

		if output.Interactive() {
			stack := tui.NewStack()

			ctx = tui.SetStackInContext(ctx, stack)
		}

		cmd.SetContext(ctx)

		return nil
	},

	PersistentPostRunE: func(cmd *cobra.Command, args []string) error {
		ctx := cmd.Context()

		output := command.GetFormatFromContext(ctx)
		if output.Interactive() {
			stack := tui.GetStackFromContext(ctx)
			if stack == nil {
				return nil
			}

			var m tea.Model = stack

			if cmd.Name() != workspaceSetCmd.Name() {
				if !config.IsWorkspaceSet() {
					m = tui.NewConfigWrapper(m, "Set Workspace", views.NewWorkspaceView(ctx, views.ListWorkspaceInput{}))
				}
			}

			if cmd.Name() != loginCmd.Name() {
				m = tui.NewConfigWrapper(m, "Login", views.NewLoginView(ctx))
			}

			p := tea.NewProgram(m, tea.WithAltScreen())
			_, err := p.Run()
			if err != nil {
				panic(fmt.Sprintf("Failed to initialize interface. Use -o to specify a non-interactive output mode: %v", err))
			}
			return nil
		}

		return nil
	},
}

func isPipe() bool {
	stdout, err := os.Stdout.Stat()
	if err != nil {
		return false
	}

	isTerminal := (stdout.Mode() & os.ModeCharDevice) == os.ModeCharDevice
	return !isTerminal
}

func isCI() bool {
	ci := os.Getenv("CI")
	return ci == "true" || ci == "1"
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.
	rootCmd.AddGroup(AllGroups...)

	rootCmd.Version = cfg.Version
	rootCmd.CompletionOptions.DisableDefaultCmd = true
	rootCmd.PersistentFlags().StringP("output", "o", "interactive", "interactive, json, yaml, or text")
	rootCmd.PersistentFlags().Bool(command.ConfirmFlag, false, "set to skip confirmation prompts")

	// Flags from the old CLI that we error with a helpful message
	rootCmd.PersistentFlags().Bool("pretty-json", false, "use --output json instead")
	if err := rootCmd.PersistentFlags().MarkHidden("pretty-json"); err != nil {
		panic(err)
	}
	rootCmd.PersistentFlags().Bool("json-record-per-line", false, "use --output json instead")
	if err := rootCmd.PersistentFlags().MarkHidden("json-record-per-line"); err != nil {
		panic(err)
	}
}

// checkForDeprecatedFlagUsage checks for usage of deprecated flags and returns an error with the new flag if found.
// These can be removed after a few months.
func checkForDeprecatedFlagUsage(cmd *cobra.Command) error {
	prettyFlag, err := cmd.Flags().GetBool("pretty-json")
	if err == nil && prettyFlag {
		return errors.New("use `--output json` instead of `--pretty-json`")
	}

	recordPerLineFlag, err := cmd.Flags().GetBool("json-record-per-line")
	if err == nil && recordPerLineFlag {
		return errors.New("use `--output json` instead of `--json-record-per-line`")
	}

	// used in services command
	serviceID, err := cmd.Flags().GetString("service-id")
	if err == nil && serviceID != "" {
		return errors.New("provide service ID as an argument instead of using the --service-id flag")
	}

	return nil
}

// RootCmd is set to export the root command for use in tests
var RootCmd = rootCmd
