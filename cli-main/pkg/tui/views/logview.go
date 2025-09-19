package views

import (
	"context"
	"fmt"
	"slices"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/help"
	"github.com/charmbracelet/bubbles/key"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/huh"
	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/x/ansi"
	"github.com/render-oss/cli/pkg/keyvalue"
	"github.com/render-oss/cli/pkg/postgres"
	"github.com/render-oss/cli/pkg/service"
	"github.com/render-oss/cli/pkg/style"
	"github.com/render-oss/cli/pkg/tui/layouts"
	"github.com/spf13/cobra"

	"github.com/render-oss/cli/pkg/client"
	lclient "github.com/render-oss/cli/pkg/client/logs"
	"github.com/render-oss/cli/pkg/command"
	"github.com/render-oss/cli/pkg/config"
	"github.com/render-oss/cli/pkg/logs"
	"github.com/render-oss/cli/pkg/pointers"
	"github.com/render-oss/cli/pkg/resource"
	"github.com/render-oss/cli/pkg/tui"
)

var (
	enter      = key.NewBinding(key.WithKeys("enter"), key.WithHelp("enter", "submit"))
	esc        = key.NewBinding(key.WithKeys("esc"), key.WithHelp("esc", "close menu"))
	openFilter = key.NewBinding(key.WithKeys("/"), key.WithHelp("/", "filter"))

	filterKeyBinds = []key.Binding{enter, esc}
)

const (
	sidebarWidth = 60
	footerHeight = 4
)

type LogInput struct {
	ResourceIDs []string `cli:"resources"`
	Instance    []string `cli:"instance"`
	Text        []string `cli:"text"`
	Level       []string `cli:"level"`
	Type        []string `cli:"type"`

	StartTime *command.TimeOrRelative `cli:"start"`
	EndTime   *command.TimeOrRelative `cli:"end"`

	Host       []string `cli:"host"`
	StatusCode []string `cli:"status-code"`
	Method     []string `cli:"method"`
	Path       []string `cli:"path"`

	Limit     int    `cli:"limit"`
	Direction string `cli:"direction"`
	Tail      bool   `cli:"tail"`

	ListResourceInput ListResourceInput
}

func getResourceIDsFromIDOrNames(ctx context.Context, c *client.ClientWithResponses, idOrNames []string) ([]string, error) {
	serviceRepo := service.NewRepo(c)
	kvRepo := keyvalue.NewRepo(c)
	postgresRepo := postgres.NewRepo(c)

	resourceIds := make([]string, len(idOrNames))

	for i, idOrName := range idOrNames {
		if matchesResourceId(idOrName) {
			// This will error out if we have a name that looks like a resource ID but isn't one.
			// Ideally we'd like to catch that case and allow looking up by name for such resources.
			// However, checking if the resource ID is valid would be a performance hit, and doesn't
			// seem worth it considering how unlikely such a name is.
			resourceIds[i] = idOrName
			continue
		}

		// We have a name, not an ID. See if we can find a match

		services, err := serviceRepo.ListServices(ctx, &client.ListServicesParams{
			Name: &client.NameParam{idOrName},
		})
		if err != nil {
			return nil, err
		}

		if len(services) == 1 {
			resourceIds[i] = services[0].Id
			continue
		}

		kvs, err := kvRepo.ListKeyValue(ctx, &client.ListKeyValueParams{
			Name: &client.NameParam{idOrName},
		})
		if err != nil {
			return nil, err
		}

		if len(kvs) == 1 {
			resourceIds[i] = kvs[0].Id
			continue
		}

		postgreses, err := postgresRepo.ListPostgres(ctx, &client.ListPostgresParams{
			Name: &client.NameParam{idOrName},
		})
		if err != nil {
			return nil, err
		}

		if len(postgreses) == 1 {
			resourceIds[i] = postgreses[0].Id
			continue
		}

		return nil, fmt.Errorf("no resource found with ID or name '%s'", idOrName)
	}

	return resourceIds, nil
}

func (l LogInput) ToParam(ctx context.Context, c *client.ClientWithResponses) (*client.ListLogsParams, error) {
	ownerID, err := config.WorkspaceID()
	if err != nil {
		return nil, fmt.Errorf("error getting workspace ID: %v", err)
	}

	if l.Limit == 0 {
		l.Limit = 100
	}

	var startTime *time.Time
	if l.StartTime != nil {
		startTime = l.StartTime.T
	}

	var endTime *time.Time
	if l.EndTime != nil {
		endTime = l.EndTime.T
	}

	resourceIDs, err := getResourceIDsFromIDOrNames(ctx, c, l.ResourceIDs)
	if err != nil {
		return nil, err
	}

	return &client.ListLogsParams{
		Resource:   resourceIDs,
		OwnerId:    ownerID,
		Instance:   pointers.FromArray(l.Instance),
		Limit:      pointers.From(l.Limit),
		StartTime:  startTime,
		EndTime:    endTime,
		Text:       pointers.FromArray(l.Text),
		Level:      pointers.FromArray(l.Level),
		Type:       pointers.FromArray(l.Type),
		Host:       pointers.FromArray(l.Host),
		StatusCode: pointers.FromArray(l.StatusCode),
		Method:     pointers.FromArray(l.Method),
		Path:       pointers.FromArray(l.Path),
		Direction:  pointers.From(mapDirection(l.Direction)),
	}, nil
}

func mapDirection(direction string) lclient.LogDirection {
	switch direction {
	case "forward":
		return lclient.Forward
	case "backward":
		return lclient.Backward
	default:
		return lclient.Backward
	}
}

type LogsView struct {
	resourceTable *ResourceView

	tabModel    *tui.TabModel
	logModel    *tui.LogModel
	footerModel *FooterModel

	layout *layouts.SidebarLayout

	onFilter    func() tea.Cmd
	isSearching bool
}

type FooterModel struct {
	help   func() string
	width  int
	height int
}

func (f *FooterModel) Init() tea.Cmd {
	return nil
}

func (f *FooterModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return f, nil
}

func (f *FooterModel) View() string {
	dividingLine := lipgloss.NewStyle().Foreground(style.ColorBorder).Render(strings.Repeat("─", f.width))

	footerText := ansi.Wrap(f.help(), f.width, "-")

	// Keep the footer a constant height
	footerStyle := lipgloss.NewStyle().Height(f.height).Width(f.width)

	return footerStyle.Render(lipgloss.JoinVertical(lipgloss.Left, dividingLine, footerText))
}

func (f *FooterModel) SetWidth(width int) {
	f.width = width
}

func (f *FooterModel) SetHeight(height int) {
	f.height = height
}

func LoadLogData(ctx context.Context, in LogInput) (*tui.LogResult, error) {
	c, err := client.NewDefaultClient()
	if err != nil {
		return nil, err
	}

	logRepo := logs.NewLogRepo(c)
	params, err := in.ToParam(ctx, c)
	if err != nil {
		return nil, fmt.Errorf("error processing arguments: %v", err)
	}

	if in.Tail {
		logChan, err := logRepo.TailLogs(ctx, params)
		if err != nil {
			return nil, fmt.Errorf("error tailing logs: %v", err)
		}
		return &tui.LogResult{Logs: &client.Logs200Response{}, LogChannel: logChan}, nil
	}

	logs, err := logRepo.ListLogs(ctx, params)
	if err != nil {
		return nil, fmt.Errorf("error listing logs: %v", err)
	}
	return &tui.LogResult{Logs: logs, LogChannel: nil}, nil
}

type tabDefinition struct {
	TabName    string
	FieldNames []string
}

func tabModel(fields []huh.Field) *tui.TabModel {
	tabDefinitions := []tabDefinition{
		{TabName: "Filter", FieldNames: []string{"resources", "instance", "text", "level", "type"}},
		{TabName: "Time", FieldNames: []string{"start", "end"}},
		{TabName: "Request", FieldNames: []string{"host", "status-code", "method", "path"}},
		{TabName: "Query", FieldNames: []string{"limit", "direction", "tail"}},
	}

	var tabs []*tui.Tab
	for _, tabDefinition := range tabDefinitions {
		tab := &tui.Tab{
			Name: tabDefinition.TabName,
		}

		var fieldsForTab []huh.Field
		for _, field := range fields {
			if slices.Contains(tabDefinition.FieldNames, field.GetKey()) {
				fieldsForTab = append(fieldsForTab, field)
			}
		}

		content := formFromFields(fieldsForTab)
		tab.Content = content

		tabs = append(tabs, tab)
	}

	return tui.NewTabModel(tabs)
}

func formFromFields(fields []huh.Field) *tui.Form {
	keyMap := huh.NewDefaultKeyMap()
	keyMap.Input.Next = key.NewBinding(key.WithKeys("tab"), key.WithHelp("tab", "next"))
	keyMap.Select.Next = key.NewBinding(key.WithKeys("tab"), key.WithHelp("tab", "next"))
	keyMap.Select.Filter = key.NewBinding()
	keyMap.MultiSelect.Next = key.NewBinding(key.WithKeys("tab"), key.WithHelp("tab", "next"))
	keyMap.MultiSelect.Toggle = key.NewBinding(key.WithKeys(" "), key.WithHelp("space", "toggle"))
	keyMap.MultiSelect.Filter = key.NewBinding()

	return tui.NewForm(huh.NewForm(huh.NewGroup(fields...)).WithKeyMap(keyMap).WithShowHelp(false))
}

func NewLogsView(
	ctx context.Context,
	logsCmd *cobra.Command,
	interactiveLogsCommand func(ctx context.Context, input LogInput, breadcrumb string) tea.Cmd,
	input LogInput,
	loadLogFunc func(ctx context.Context, in LogInput) (*tui.LogResult, error),
	opts ...tui.TableOption[resource.Resource],
) *LogsView {
	view := &LogsView{}

	// If no resources specified, show resource selection view
	if len(input.ResourceIDs) == 0 {
		view.resourceTable = NewResourceView(ctx, input.ListResourceInput, func(r resource.Resource) tea.Cmd {
			input.ResourceIDs = []string{r.ID()}
			return interactiveLogsCommand(ctx, input, resource.BreadcrumbForResource(r))
		}, opts...)
	} else {
		// Create log filter form
		fields, result := command.HuhFormFields(logsCmd, &input)

		tabs := tabModel(fields)
		view.onFilter = func() tea.Cmd {
			var logInput LogInput
			err := command.StructFromFormValues(result, &logInput)
			if err != nil {
				return func() tea.Msg { return tui.ErrorMsg{Err: fmt.Errorf("failed to parse form values: %w", err)} }
			}

			return interactiveLogsCommand(ctx, logInput, "") // we don't need a breadcrumb for the filter window
		}
		view.tabModel = tabs

		// Create log view model
		view.logModel = tui.NewLogModel(command.LoadCmd(ctx, loadLogFunc, input))
		view.footerModel = &FooterModel{help: view.logsHelp}
		view.layout = layouts.NewSidebarLayout(layouts.NewBoxLayout(lipgloss.NewStyle().PaddingRight(1), view.tabModel), view.logModel, view.footerModel)
		view.layout.SetSidebarWidth(sidebarWidth)
		view.layout.SetFooterHeight(footerHeight)
	}

	return view
}

func (v *LogsView) Init() tea.Cmd {
	if v.resourceTable != nil {
		return v.resourceTable.Init()
	}
	return v.layout.Init()
}

func (v *LogsView) filterHelp() string {
	keys := append(v.tabModel.KeyBinds(), filterKeyBinds...)

	currentTab := v.tabModel.CurrentTab().Content
	if form, ok := currentTab.(*tui.Form); ok {
		keys = append(keys, form.KeyBinds()...)
	}

	return help.New().ShortHelpView(keys)
}

func (v *LogsView) logsHelp() string {
	keys := append(v.logModel.KeyBinds(), openFilter)

	return help.New().ShortHelpView(keys)
}

func (v *LogsView) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	if v.resourceTable != nil {
		_, cmd := v.resourceTable.Update(msg)
		return v, cmd
	}

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.Type {
		case tea.KeyEnter:
			return v, v.onFilter()
		default:
			if k := msg.String(); k == "/" && !v.isSearching {
				v.isSearching = true
				v.footerModel.help = v.filterHelp
				v.layout.SetSidebarVisible(true)
				// Return nil to prevent the filter from handling the keypress
				return v, nil
			}
		}
	case *tui.BackMsg:
		if v.isSearching {
			msg.Handled = true
			v.isSearching = false
			v.footerModel.help = v.logsHelp
			v.layout.SetSidebarVisible(false)
		}
	}

	_, cmd := v.layout.Update(msg)
	return v, cmd
}

func (v *LogsView) View() string {
	if v.resourceTable != nil {
		return v.resourceTable.View()
	}
	return v.layout.View()
}
