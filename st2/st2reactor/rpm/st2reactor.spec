%define package st2reactor
%include ../rpmspec/st2pkg_toptags.spec

Summary: St2Reactor - StackStorm sensors component
Requires: st2common = %{version}-%{release}

%description
  <insert long description, indented with spaces>

%install
  %default_install
  %pip_install_venv

  # systemd service file
  mkdir -p %{buildroot}%{_unitdir}
  install -m0644 %{SOURCE0}/rpm/st2rulesengine.service %{buildroot}%{_unitdir}/st2rulesengine.service
  install -m0644 %{SOURCE0}/rpm/st2sensorcontainer.service %{buildroot}%{_unitdir}/st2sensorcontainer.service
  make post_install DESTDIR=%{?buildroot}

%prep
  rm -rf %{buildroot}
  mkdir -p %{buildroot}

%clean
  rm -rf %{buildroot}

%post
  %systemd_post st2rulesengine st2sensorcontainer
  systemctl --no-reload enable st2rulesengine st2sensorcontainer >/dev/null 2>&1 || :

%preun
  %systemd_preun st2rulesengine st2sensorcontainer

%postun
  %systemd_postun

%files
  %{_bindir}/*
  %{_datadir}/python/%{name}
  %config(noreplace) %{_sysconfdir}/st2/*
  %{_unitdir}/st2rulesengine.service
  %{_unitdir}/st2sensorcontainer.service